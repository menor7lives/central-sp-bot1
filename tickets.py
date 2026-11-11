"""Sistema de tickets: painel, categorias, transcrição e avaliação."""
import re

import discord

import dados

CARGO_ATENDENTE = "🎫・Atendente"
CATEGORIA_CANAL = "🎫・ATENDIMENTO"

CATEGORIAS = {
    "suporte": {"emoji": "🛠️", "nome": "Suporte", "cor": 0x5865F2},
    "duvida": {"emoji": "❓", "nome": "Dúvida", "cor": 0x3498DB},
    "denuncia": {"emoji": "🚨", "nome": "Denúncia", "cor": 0xE74C3C},
    "comercial": {"emoji": "💼", "nome": "Comercial", "cor": 0xF1C40F},
}


async def cargo_atendente(guild):
    r = discord.utils.get(guild.roles, name=CARGO_ATENDENTE)
    if r is None:
        r = await guild.create_role(
            name=CARGO_ATENDENTE, color=discord.Color(0xF1C40F),
            reason="Slayer Bot — sistema de tickets")
    return r


async def _overwrites_base(guild, atendente):
    return {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        atendente: discord.PermissionOverwrite(
            view_channel=True, send_messages=True, read_message_history=True,
            manage_messages=True, attach_files=True),
        guild.me: discord.PermissionOverwrite(
            view_channel=True, send_messages=True, manage_channels=True,
            read_message_history=True),
    }


async def categoria_atendimento(guild):
    """Garante cargo de atendente + categoria de tickets (cria se não existir)."""
    atendente = await cargo_atendente(guild)
    over = await _overwrites_base(guild, atendente)
    cat = discord.utils.get(guild.categories, name=CATEGORIA_CANAL)
    if cat is None:
        cat = await guild.create_category(
            CATEGORIA_CANAL, overwrites=over, reason="Slayer Bot — tickets")
    else:
        try:
            await cat.edit(overwrites=over, reason="Slayer Bot — tickets")
        except (discord.Forbidden, discord.HTTPException):
            pass
    return cat, atendente


async def abrir(guild, user, cat_key: str, assunto: str):
    """Cria o canal do ticket. Retorna (canal, embed de boas-vindas)."""
    info = CATEGORIAS[cat_key]
    cat, atendente = await categoria_atendimento(guild)
    over = await _overwrites_base(guild, atendente)
    over[user] = discord.PermissionOverwrite(
        view_channel=True, send_messages=True, read_message_history=True,
        attach_files=True)
    nome = re.sub(r"[^a-z0-9]", "", user.name.lower())[:16] or "membro"
    canal = await guild.create_text_channel(
        f"🎫・ticket-{nome}", category=cat, overwrites=over,
        topic=f"Ticket de {user.id} | {info['nome']} | {(assunto or '')[:100]}",
        reason="Slayer Bot — novo ticket")
    e = discord.Embed(
        title=f"{info['emoji']} Ticket — {info['nome']}",
        description=(
            f"**Solicitante:** {user.mention}\n"
            f"**Assunto:** {assunto or '—'}\n\n"
            "Descreva seu problema com detalhes aqui. "
            "A equipe de atendimento já foi avisada e vai te responder.\n\n"
            "🔒 Quando resolver, clique no botão abaixo pra fechar."),
        color=info["cor"])
    e.set_thumbnail(url=user.display_avatar.url)
    e.set_footer(text=f"Slayer Bot • {guild.name}")
    return canal, e


def opener_id(channel):
    """Extrai o ID do solicitante do tópico do canal."""
    try:
        topo = (channel.topic or "").split("|")[0]
        return int(topo.replace("Ticket de", "").strip())
    except Exception:
        return None


async def transcrever(channel, limite=300):
    """Histórico do ticket em texto. Retorna (nome_arquivo, bytes)."""
    linhas = []
    try:
        async for m in channel.history(limit=limite, oldest_first=True):
            conteudo = (m.content or "").strip()
            if conteudo:
                t = m.created_at.strftime("%d/%m/%Y %H:%M")
                linhas.append(f"[{t}] {m.author}: {conteudo}")
    except discord.HTTPException:
        pass
    texto = "\n".join(linhas) or "(sem mensagens)"
    return f"transcricao-ticket-{channel.name}.txt", texto.encode("utf-8")


def avaliar(gid, nota: int):
    """Registra nota 1-5 do atendimento. Retorna (media, total)."""
    nota = max(1, min(5, int(nota)))
    g = dados.get(gid)
    g["avaliacoes"].append(nota)
    dados.salvar()
    notas = g["avaliacoes"]
    return round(sum(notas) / len(notas), 1), len(notas)


def painel_embed(guild, cor=0x5865F2):
    linhas = "\n".join(f"> {i['emoji']} **{i['nome']}**" for i in CATEGORIAS.values())
    e = discord.Embed(
        title="🎫 Central de Atendimento",
        description=(
            "Precisa de ajuda? **Abra um ticket** clicando num botão abaixo.\n\n"
            f"{linhas}\n\n"
            "⚠️ Abusos do sistema = advertência ou ban."),
        color=cor)
    e.set_footer(text="Slayer Bot • atendimento profissional")
    return e
