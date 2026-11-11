"""Armazenamento central do Slayer Bot — dados por servidor + licenças.

Salva num arquivo JSON (rápido) e faz backup automático no privado do
dono do bot (durável): se a hospedagem reiniciar do zero (redeploy),
os dados são recuperados do histórico do privado automaticamente.
"""
import io
import json
import os
import time

import discord

import config

_PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.path.join(_PASTA, "slayer_dados.json")

# módulos que o comprador pode ligar/desligar por servidor
MODULOS = {
    "seguranca": "🛡️ Proteção (anti-raid, anti-spam, anti-link)",
    "moderacao": "⚖️ Moderação (advertências, ban, kick, timeout)",
    "tickets": "🎫 Atendimento por tickets",
    "automacao": "⚙️ Automação (boas-vindas, autorole, logs)",
    "sugestoes": "💡 Sugestões e denúncias",
    "automaticas": "📨 Mensagens automáticas",
}

PADRAO = {
    "modulos": {k: True for k in MODULOS},
    "seguranca": {"antiraid": True, "antispam": True, "antilink": True,
                  "antibot": False, "raid_ate": 0},
    "premium_expira": 0,
    "cor": None,
    "apelido": None,
    "rodape": None,
    "separador": None,
    "personalidade": None,
    "boas_vindas": {},          # {"canal": id, "mensagem": str}
    "autorole": None,
    "canal_logs": None,
    "canal_sugestoes": None,
    "canal_denuncias": None,
    "advertencias": {},         # {uid: [{motivo, por, quando}]}
    "memoria_ativa": True,
    "memoria": {},              # {uid: [{r: pergunta, s: resposta}]}
    "contadores": {"mensagens": 0, "entradas": 0},
    "automaticas": [],          # [{canal, mensagem, intervalo_h, proxima}]
    "avaliacoes": [],           # notas de tickets [1..5]
}

_dados = {"guilds": {}, "chaves": {}}
_pendentes = 0


def _copia(valor):
    return json.loads(json.dumps(valor))


def _carregar():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            lido = json.load(f)
        _dados["guilds"] = lido.get("guilds", {})
        _dados["chaves"] = lido.get("chaves", {})
    except Exception:
        pass


_carregar()


def chaves() -> dict:
    """Licenças geradas: {chave: {dias, usada, guild}}."""
    return _dados["chaves"]


def todos() -> dict:
    """Todos os servidores com dados salvos."""
    return _dados["guilds"]


def get(gid) -> dict:
    """Dados de um servidor (cria com valores padrão se não existir)."""
    gid = str(gid)
    g = _dados["guilds"].get(gid)
    if g is None:
        g = _copia(PADRAO)
        _dados["guilds"][gid] = g
    else:
        # garante campos novos mesmo depois de atualização do bot
        for k, v in PADRAO.items():
            if k not in g:
                g[k] = _copia(v) if isinstance(v, (dict, list)) else v
    return g


def salvar():
    for g in _dados["guilds"].values():
        g["_ts"] = time.time()
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(_dados, f, ensure_ascii=False)
    except Exception as e:
        print(f"(erro ao salvar dados: {e})")


def definir(gid, **campos):
    g = get(gid)
    g.update(campos)
    salvar()
    return g


def eh_modulo(gid, nome) -> bool:
    return get(gid)["modulos"].get(nome, True)


def contar(gid, campo):
    """Conta eventos (mensagens, entradas) sem gravar em disco toda hora."""
    global _pendentes
    g = get(gid)
    g["contadores"][campo] = g["contadores"].get(campo, 0) + 1
    _pendentes += 1
    if _pendentes >= 25:
        _pendentes = 0
        salvar()


# ---------------- backup no privado do dono (durável) ----------------
_NAO_BACKUP = ("contadores", "memoria", "_ts")


async def _dm_dono(bot):
    if not config.OWNER_ID:
        return None
    try:
        user = bot.get_user(config.OWNER_ID) or await bot.fetch_user(config.OWNER_ID)
        return await user.create_dm()
    except Exception:
        return None


async def registrar_dm(bot, gid):
    """Copia os dados do servidor pro privado do dono (durável contra redeploys)."""
    dm = await _dm_dono(bot)
    if dm is None:
        return
    g = {k: v for k, v in get(gid).items() if k not in _NAO_BACKUP}
    payload = json.dumps(g, ensure_ascii=False)
    try:
        await dm.send(
            content=f"SLAYERDATA|{gid}|{int(time.time())}",
            file=discord.File(io.BytesIO(payload.encode("utf-8")),
                              filename=f"slayer-{gid}.json"))
    except Exception:
        pass


async def dm_chave(bot, chave, dias, usada, guild=None):
    """Registra uma licença no privado do dono (histórico durável)."""
    dm = await _dm_dono(bot)
    if dm is None:
        return
    try:
        await dm.send(f"SLAYERKEY|{chave}|{dias}|{int(usada)}|{guild or 0}")
    except Exception:
        pass


async def recuperar_dm(bot) -> int:
    """Reconstrói licenças e configurações do histórico do privado do dono."""
    dm = await _dm_dono(bot)
    if dm is None:
        return 0
    recuperados = 0
    vistos = set()
    try:
        async for msg in dm.history(limit=500):
            conteudo = msg.content or ""
            if conteudo.startswith("SLAYERDATA|"):
                partes = conteudo.split("|")
                gid = partes[1]
                if gid in vistos:
                    continue
                vistos.add(gid)
                local = _dados["guilds"].get(gid)
                ts_local = float((local or {}).get("_ts") or 0)
                # o histórico é do mais novo pro mais velho
                if local is not None and ts_local >= msg.created_at.timestamp():
                    continue  # arquivo local já é mais novo
                if not msg.attachments:
                    continue
                try:
                    dados_g = json.loads(await msg.attachments[0].read())
                    _dados["guilds"][gid] = dados_g
                    recuperados += 1
                except Exception:
                    pass
            elif conteudo.startswith("SLAYERKEY|"):
                partes = conteudo.split("|")
                if len(partes) >= 5:
                    chave, dias, usada, guild = partes[1], partes[2], partes[3], partes[4]
                    info = _dados["chaves"].setdefault(
                        chave, {"dias": int(dias), "usada": False, "guild": None})
                    info["dias"] = int(dias)
                    if usada == "1":
                        info["usada"] = True
                        info["guild"] = None if guild in ("0", "") else guild
    except Exception as e:
        print(f"(recuperação de dados falhou: {e})")
    if recuperados:
        salvar()
    return recuperados
