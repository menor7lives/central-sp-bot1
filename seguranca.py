"""Proteção automática: anti-raid, anti-spam/flood, anti-link e anti-bot."""
import re
import time
from collections import defaultdict, deque

import discord

import dados

RAID_JANELA = 10       # segundos de janela
RAID_LIMITE = 8        # entradas na janela pra considerar raid
RAID_MINUTOS = 5       # duração do modo de proteção
SPAM_JANELA = 4
SPAM_LIMITE = 6        # mensagens na janela = flood
CONTAS_NOVAS_DIAS = 3  # conta "recém-criada" (anti-bot)
PUNICAO_SPAM_SEG = 90
PUNICAO_LINK_MIN = 10

REGEX_CONVITE = re.compile(
    r"(?:https?://)?(?:discord\.(?:gg|com/invite|app/invite)|dsc\.gg)/[\w-]+", re.I)

_joins = defaultdict(deque)
_msgs = defaultdict(deque)
_infracoes = defaultdict(deque)


def conta_nova(member, dias) -> bool:
    try:
        return (discord.utils.utcnow() - member.created_at).days < dias
    except Exception:
        return False


async def verificar_entrada(member):
    """Anti-raid + anti-bot. Retorna [(nivel, texto)] pra registrar nos logs."""
    eventos = []
    guild = member.guild
    cfg = dados.get(guild.id)["seguranca"]
    agora = time.time()

    j = _joins[guild.id]
    j.append(agora)
    while j and agora - j[0] > RAID_JANELA:
        j.popleft()

    if cfg.get("antiraid") and len(j) >= RAID_LIMITE:
        cfg["raid_ate"] = agora + RAID_MINUTOS * 60
        dados.salvar()
        eventos.append((
            "raid",
            f"🚨 **RAID detectado!** {len(j)} membros entraram em {RAID_JANELA}s.\n"
            f"Modo de proteção ativo por **{RAID_MINUTOS} minutos** — contas novas serão expulsas."))

    if agora < float(cfg.get("raid_ate") or 0):
        if conta_nova(member, 30):
            try:
                await member.kick(reason="Slayer Bot — proteção anti-raid")
                eventos.append((
                    "kick",
                    f"👢 {member.mention} expulso pelo anti-raid (conta criada há menos de 30 dias)."))
            except discord.Forbidden:
                eventos.append((
                    "erro",
                    "⚠️ Sem permissão pra expulsar durante o raid (preciso de **Expulsar membros**)."))
        return eventos

    if cfg.get("antibot") and conta_nova(member, CONTAS_NOVAS_DIAS):
        eventos.append((
            "alerta",
            f"🕵️ {member.mention} entrou com conta criada há menos de {CONTAS_NOVAS_DIAS} dias."))
    return eventos


async def verificar_mensagem(message):
    """Anti-spam e anti-link. Retorna (acao, detalhe).

    acao: None (tudo certo) | "apagar" | "timeout"
    """
    if not message.guild:
        return None, ""
    autor = message.author
    if autor.bot:
        return None, ""
    perms = getattr(autor, "guild_permissions", None)
    if perms is not None and (perms.administrator or perms.manage_guild):
        return None, ""  # staff não é punido

    cfg = dados.get(message.guild.id)["seguranca"]
    agora = time.time()

    m = _msgs[(message.guild.id, autor.id)]
    m.append(agora)
    while m and agora - m[0] > SPAM_JANELA:
        m.popleft()
    total = len(m)
    if cfg.get("antispam") and total > SPAM_LIMITE:
        m.clear()
        return "timeout", f"spam/flood ({total} mensagens em {SPAM_JANELA}s)"

    if cfg.get("antilink") and REGEX_CONVITE.search(message.content or ""):
        return "apagar", "link de convite do Discord"

    return None, ""


def registrar_infracao(gid, uid) -> bool:
    """Conta infrações (ex.: links proibidos). True = chegou no limite (3)."""
    agora = time.time()
    dq = _infracoes[(gid, uid)]
    dq.append(agora)
    while dq and agora - dq[0] > 600:  # janela de 10 minutos
        dq.popleft()
    return len(dq) >= 3
