"""Sistema de licenças Premium do Slayer Bot — feito pra revenda.

Cada chave vale para 1 servidor. Exemplo de venda:
  1. Dono gera a chave:  /gerarkey dias:30
  2. Cliente recebe a chave e ativa:  /ativar
  3. Chaves usadas em outro servidor são recusadas.
"""
import random
import time

import dados

# sem 0/O/1/I/L pra ninguém digitar errado
ALFABETO = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def gerar_chave(dias: int = 30) -> str:
    partes = ["".join(random.choices(ALFABETO, k=5)) for _ in range(3)]
    chave = "SLY-" + "-".join(partes)
    dados.chaves()[chave] = {"dias": int(dias), "usada": False, "guild": None}
    dados.salvar()
    return chave


def ativar(gid, chave: str):
    """Ativa uma licença neste servidor. Retorna (ok, mensagem)."""
    gid = str(gid)
    chave = (chave or "").strip().upper()
    info = dados.chaves().get(chave)
    if info is None:
        return False, ("❌ **Chave inválida!** Confira se digitou certinho "
                       "(ex.: `SLY-XXXXX-XXXXX-XXXXX`).")
    if info.get("usada") and info.get("guild") == gid:
        return False, "⚠️ Essa chave **já está ativa** neste servidor."
    if info.get("usada"):
        return False, ("❌ Essa chave já foi usada em **outro servidor**. "
                       "Cada chave vale para 1 servidor.")
    g = dados.get(gid)
    base = max(time.time(), float(g.get("premium_expira") or 0))
    g["premium_expira"] = base + int(info.get("dias", 30)) * 86400
    info["usada"] = True
    info["guild"] = gid
    dados.salvar()
    return True, f"👑 **Premium ativado até {expira_str(gid)}!**"


def expira(gid) -> float:
    return float(dados.get(gid).get("premium_expira") or 0)


def eh_premium(gid) -> bool:
    return expira(gid) > time.time()


def expira_str(gid):
    ts = expira(gid)
    if not ts:
        return None
    return time.strftime("%d/%m/%Y", time.localtime(ts))


def dias_restantes(gid) -> int:
    return max(0, int((expira(gid) - time.time()) // 86400))


def licencas_ativas():
    """[(gid, timestamp_expira)] de todos os servidores com premium ativo."""
    agora = time.time()
    return [(gid, g.get("premium_expira") or 0)
            for gid, g in dados.todos().items()
            if (g.get("premium_expira") or 0) > agora]


def chaves_disponiveis():
    return {c: i for c, i in dados.chaves().items() if not i.get("usada")}
