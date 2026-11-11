"""Automação: boas-vindas, autorole, logs, sugestões, denúncias e mensagens automáticas."""
import time

import discord

import dados


def mensagem_boas_vindas(member, texto: str) -> str:
    return ((texto or "Bem-vindo, {membro}! 👋")
            .replace("{membro}", member.mention)
            .replace("{nome}", member.display_name)
            .replace("{servidor}", member.guild.name))


def embed_boas_vindas(member, texto: str, cor=0x5865F2):
    e = discord.Embed(
        title=f"👋 Bem-vindo ao {member.guild.name}!",
        description=mensagem_boas_vindas(member, texto),
        color=cor)
    e.set_thumbnail(url=member.display_avatar.url)
    e.set_footer(text=f"Membro #{member.guild.member_count} • Slayer Bot")
    return e


async def aplicar_autorole(member):
    gid = member.guild.id
    cargo_id = dados.get(gid).get("autorole")
    if not cargo_id:
        return
    cargo = member.guild.get_role(int(cargo_id))
    if cargo is None:
        return
    try:
        await member.add_roles(cargo, reason="Slayer Bot — autorole")
    except (discord.Forbidden, discord.HTTPException):
        pass


def log_embed(titulo, cor, descricao):
    return discord.Embed(title=titulo, description=descricao[:2000], color=cor,
                         timestamp=discord.utils.utcnow())


async def logar(bot, guild, embed):
    if guild is None:
        return
    canal_id = dados.get(guild.id).get("canal_logs")
    if not canal_id:
        return
    canal = bot.get_channel(int(canal_id))
    if canal is None:
        return
    try:
        await canal.send(embed=embed)
    except (discord.Forbidden, discord.HTTPException):
        pass


def sugestao_embed(member, texto, cor=0x5865F2):
    e = discord.Embed(
        title="💡 Nova sugestão",
        description=f"{texto[:2000]}\n\n⏳ **Status:** Pendente",
        color=cor)
    e.set_author(name=f"{member.display_name}", icon_url=member.display_avatar.url)
    e.set_footer(text=f"Por {member.id} • reaja 👍👎 pra votar")
    return e


def denuncia_embed(member, alvo, motivo, cor=0xE74C3C):
    e = discord.Embed(
        title="🚨 Nova denúncia",
        description=(f"**Denunciante:** {member.mention}\n"
                     f"**Acusado:** {alvo}\n"
                     f"**Motivo:** {motivo[:1500]}"),
        color=cor)
    e.set_footer(text="Slayer Bot • canal confidencial da staff")
    return e


# ---------------- mensagens automáticas ----------------
def adicionar_automatica(gid, canal_id, mensagem, horas):
    g = dados.get(gid)
    g["automaticas"].append({
        "canal": int(canal_id),
        "mensagem": mensagem[:1500],
        "intervalo_h": float(horas),
        "proxima": time.time() + float(horas) * 3600,
    })
    dados.salvar()
    return len(g["automaticas"])


def listar_automaticas(gid):
    g = dados.get(gid)
    return g.get("automaticas", [])


def remover_automatica(gid, indice) -> bool:
    g = dados.get(gid)
    lista = g.get("automaticas", [])
    if 1 <= indice <= len(lista):
        lista.pop(indice - 1)
        dados.salvar()
        return True
    return False


def embed_automatica(texto, cor=0x5865F2):
    return discord.Embed(description=texto[:2000], color=cor,
                         timestamp=discord.utils.utcnow())


async def processar_automaticas(bot):
    """Envia as mensagens agendadas vencidas (chamado por loop no bot.py)."""
    agora = time.time()
    for gid, g in list(dados.todos().items()):
        if not g.get("modulos", {}).get("automaticas", True):
            continue
        mudou = False
        for item in g.get("automaticas", []):
            if agora >= float(item.get("proxima", 0)):
                canal = bot.get_channel(int(item["canal"]))
                if canal is not None:
                    try:
                        await canal.send(embed=embed_automatica(item["mensagem"]))
                        item["proxima"] = agora + float(item["intervalo_h"]) * 3600
                        mudou = True
                    except (discord.Forbidden, discord.HTTPException):
                        pass
                else:
                    item["proxima"] = agora + float(item["intervalo_h"]) * 3600
                    mudou = True
        if mudou:
            dados.salvar()
