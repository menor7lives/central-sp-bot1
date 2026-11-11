"""Backup e restauração da estrutura do servidor (cargos, canais e permissões)."""
import json

import discord


def _overwrites_para_dict(overwrites):
    """Converte overwrites do Discord no formato dos templates (por nome)."""
    saida = {}
    for alvo, ow in (overwrites or {}).items():
        if isinstance(alvo, discord.Role):
            if alvo.is_default():
                nome = "@everyone"
            elif alvo.managed:
                continue
            else:
                nome = alvo.name
        else:
            nome = getattr(alvo, "name", None)
            if not nome:
                continue
        allow = [p for p, v in ow if v is True]
        deny = [p for p, v in ow if v is False]
        if allow or deny:
            saida[nome] = {"allow": allow, "deny": deny}
    return saida


def _canal_dict(ch):
    tipo = "voice" if isinstance(ch, (discord.VoiceChannel, discord.StageChannel)) else "text"
    item = {"name": ch.name, "type": tipo,
            "overwrites": _overwrites_para_dict(ch.overwrites)}
    if tipo == "voice" and getattr(ch, "user_limit", None):
        item["user_limit"] = ch.user_limit
    return item


def exportar(guild):
    """Fotografia completa da estrutura → bytes JSON (mesmo formato dos templates)."""
    roles = []
    for r in guild.roles:  # ordem crescente (a primeira é @everyone)
        if r.is_default() or r.managed:
            continue
        roles.append({
            "name": r.name,
            "color": r.color.value if str(r.color) != "#000000" else 0x99AAB5,
            "hoist": r.hoist,
            "permissions": [p for p, v in r.permissions if v],
        })

    categorias = []
    for c in [x for x in guild.channels if isinstance(x, discord.CategoryChannel)]:
        categorias.append({
            "name": c.name,
            "overwrites": _overwrites_para_dict(c.overwrites),
            "channels": [_canal_dict(ch) for ch in c.channels],
        })

    # canais sem categoria entram numa categoria própria (o builder exige)
    soltos = [ch for ch in guild.channels
              if ch.category is None and not isinstance(ch, discord.CategoryChannel)]
    if soltos:
        categorias.append({"name": "📁・GERAL", "overwrites": {},
                           "channels": [_canal_dict(ch) for ch in soltos]})

    data = {"name": guild.name, "roles": roles, "categories": categorias}
    return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")


def validar(data) -> bool:
    """Confere se o JSON tem cara de backup do Slayer."""
    return (isinstance(data, dict)
            and isinstance(data.get("roles"), list)
            and isinstance(data.get("categories"), list))
