
"""Slayer Bot — o bot que monta servidores e sites por menção."""

import os
import sys

# Corrige acentos e emojis no console do Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import discord
from aiohttp import web
from discord import app_commands
from discord.ext import commands

import ai
import builder
import logo
import sitegen
from templates import TEMPLATES, get_template
import config


intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)


def can_build(member: discord.Member) -> bool:
    """Verifica se o usuário pode criar estruturas."""
    return (
        member.guild_permissions.administrator
        or member.guild_permissions.manage_guild
        or member.id == config.OWNER_ID
    )


# ============================================================
# CONSTRUÇÃO DE SERVIDORES
# ============================================================

async def run_build(
    interaction_or_msg,
    template_key=None,
    spec=None,
    guild=None
):
    """Cria a estrutura do servidor sem apagar os canais existentes."""

    is_interaction = isinstance(
        interaction_or_msg,
        discord.Interaction
    )

    if guild is None:
        guild = interaction_or_msg.guild

    if guild is None:
        return

    origin = interaction_or_msg.channel

    requester = (
        interaction_or_msg.user
        if is_interaction
        else interaction_or_msg.author
    )

    if spec is None:
        spec = get_template(template_key or "comunidade")

    if spec is None:
        return await origin.send(
            "❌ Não consegui encontrar esse modelo de servidor."
        )

    try:
        await origin.send(
            "⚔️ **Slayer Bot iniciou a construção!**\n"
            "Estou organizando os canais, categorias e cargos. "
            "Os itens existentes serão preservados."
        )

        async def progress(text):
            try:
                await origin.send(text)
            except discord.HTTPException:
                pass

        created = await builder.build_guild_structure(
            guild,
            spec,
            progress=progress
        )

        summary = builder.summary_embed(
            spec,
            created,
            TEMPLATES.get(
                template_key or "",
                {}
            ).get("label"),
            {"channels": 0, "roles": 0}
        )

        await origin.send(
            f"✅ <@{requester.id}>! "
            "**A estrutura do servidor foi criada com sucesso!**",
            embed=summary
        )

    except discord.Forbidden:
        await origin.send(
            "❌ **Não tenho permissões suficientes!**\n\n"
            "Verifique se meu cargo possui as permissões necessárias "
            "e se está acima dos cargos que preciso organizar."
        )

    except Exception as e:
        print(f"[ERRO AO CONSTRUIR SERVIDOR] {e}")

        await origin.send(
            "❌ Ocorreu um erro durante a construção.\n"
            "Confira o console para ver os detalhes."
        )


# ============================================================
# PAINEL DE CRIAÇÃO
# ============================================================

class TemplateSelect(discord.ui.Select):

    def __init__(self):
        options = [
            discord.SelectOption(
                label=t["label"],
                value=key,
                emoji=t["emoji"],
                description=t["desc"][:100]
            )
            for key, t in TEMPLATES.items()
        ]

        super().__init__(
            placeholder="🏗️ Escolha o modelo de servidor...",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        key = self.values[0]
        template = TEMPLATES[key]

        if not can_build(interaction.user):
            return await interaction.response.send_message(
                "❌ Você precisa da permissão "
                "**Gerenciar Servidor** para criar estruturas.",
                ephemeral=True
            )

        embed = discord.Embed(
            title=f"{template['emoji']} Criar: {template['label']}",
            description=(
                f"{template['desc']}\n\n"
                "📌 **Como funciona:**\n"
                "Vou adicionar a estrutura escolhida ao servidor, "
                "preservando os canais e cargos existentes.\n\n"
                "Clique em **Confirmar** para começar."
            ),
            color=0x5865F2
        )

        await interaction.response.send_message(
            embed=embed,
            view=ConfirmBuild(key, interaction.user.id),
            ephemeral=True
        )


class ConfirmBuild(discord.ui.View):

    def __init__(self, template_key: str, user_id: int):
        super().__init__(timeout=60)
        self.template_key = template_key
        self.user_id = user_id

    @discord.ui.button(
        label="Confirmar criação",
        style=discord.ButtonStyle.green,
        emoji="✅"
    )
    async def confirm(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if interaction.user.id != self.user_id:
            return await interaction.response.send_message(
                "❌ Só quem abriu o painel pode confirmar.",
                ephemeral=True
            )

        await interaction.response.send_message(
            "🚀 **Construção iniciada!** "
            "Estou preparando seu servidor...",
            ephemeral=True
        )

        await run_build(
            interaction,
            self.template_key
        )

    @discord.ui.button(
        label="Cancelar",
        style=discord.ButtonStyle.grey,
        emoji="✖️"
    )
    async def cancel(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.edit_message(
            content="❌ Criação cancelada.",
            view=None,
            embed=None
        )


class Dashboard(discord.ui.View):

    def __init__(self, user_id: int):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.add_item(TemplateSelect())


def dashboard_embed(guild: discord.Guild) -> discord.Embed:

    embed = discord.Embed(
        title="⚔️ Slayer Bot — Painel",
        description=(
            "Bem-vindo ao painel de criação do **Slayer Bot**!\n\n"
            "Escolha um modelo abaixo ou me mencione para pedir algo:\n\n"
            "> `@Slayer Bot crie um servidor profissional de futebol`\n"
            "> `@Slayer Bot crie um site de loja`\n\n"
            f"**Servidor:** {guild.name}\n"
            f"**Modelos disponíveis:** {len(TEMPLATES)}\n"
            f"**Tipos de sites:** {len(sitegen.TIPOS)}"
        ),
        color=0x5865F2
    )

    if bot.user:
        embed.set_thumbnail(url=bot.user.display_avatar.url)

    for key, template in TEMPLATES.items():
        embed.add_field(
            name=f"{template['emoji']} {template['label']}",
            value=template["desc"][:90],
            inline=True
        )

    embed.set_footer(
        text="Slayer Bot • criação inteligente de servidores e sites"
    )

    return embed


# ============================================================
# KEEP-ALIVE
# ============================================================

async def start_keepalive():

    """Mini servidor web para hospedagens como Render."""

    async def handler(_):
        return web.Response(
            text="⚔️ Slayer Bot está online!"
        )

    app = web.Application()
    app.router.add_get("/", handler)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.getenv("PORT", "8080"))

    await web.TCPSite(
        runner,
        "0.0.0.0",
        port
    ).start()

    print(f"🌐 Keep-alive ativo na porta {port}")


# ============================================================
# EVENTOS
# ============================================================


@bot.event
async def on_ready():
    print(f"✅ {bot.user} — Slayer Bot online!")

    try:
        if not getattr(bot, "_keepalive_started", False):
            await start_keepalive()
            bot._keepalive_started = True
    except Exception as e:
        print(f"(Keep-alive não iniciou: {e})")

    try:
        if not getattr(bot, "_commands_synced", False):

            # Remove registros antigos exclusivos de servidor
            for guild in bot.guilds:
                bot.tree.clear_commands(guild=guild)
                await bot.tree.sync(guild=guild)

            # Sincroniza os comandos globais uma única vez
            synced = await bot.tree.sync()

            print(f"✅ {len(synced)} comandos sincronizados!")
            bot._commands_synced = True

    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")



# ============================================================
# COMANDO /PAINEL
# ============================================================

@bot.tree.command(
    name="painel",
    description="⚔️ Abre o painel do Slayer Bot"
)
async def painel(interaction: discord.Interaction):

    if interaction.guild is None:
        return await interaction.response.send_message(
            "❌ Esse comando só pode ser usado em um servidor.",
            ephemeral=True
        )

    await interaction.response.send_message(
        embed=dashboard_embed(interaction.guild),
        view=Dashboard(interaction.user.id)
    )


# ============================================================
# COMANDO /CRIAR
# ============================================================

@bot.tree.command(
    name="criar",
    description="🏗️ Cria uma estrutura profissional para seu servidor"
)
@app_commands.describe(
    template="Escolha o modelo de servidor"
)
@app_commands.choices(
    template=[
        app_commands.Choice(
            name="⚽ Futebol Profissional",
            value="futebol"
        ),
        app_commands.Choice(
            name="🏘️ Comunidade",
            value="comunidade"
        ),
        app_commands.Choice(
            name="🎮 Gaming",
            value="gaming"
        ),
        app_commands.Choice(
            name="🚗 FiveM / RP",
            value="fivem"
        ),
        app_commands.Choice(
            name="🛒 Loja / E-commerce",
            value="loja"
        ),
        app_commands.Choice(
            name="🏢 Empresa / Corporação",
            value="empresa"
        ),
        app_commands.Choice(
            name="🎵 Estúdio Musical",
            value="studio"
        ),
        app_commands.Choice(
            name="🏆 Clã de E-sports",
            value="cla"
        )
    ]
)
async def criar(
    interaction: discord.Interaction,
    template: app_commands.Choice[str]
):

    if interaction.guild is None:
        return await interaction.response.send_message(
            "❌ Use esse comando dentro de um servidor.",
            ephemeral=True
        )

    if not can_build(interaction.user):
        return await interaction.response.send_message(
            "❌ Você precisa da permissão "
            "**Gerenciar Servidor** para construir estruturas.",
            ephemeral=True
        )

    await interaction.response.send_message(
        f"🚀 Construindo o modelo "
        f"**{TEMPLATES[template.value]['label']}**...\n"
        "Os canais e cargos existentes serão preservados.",
        ephemeral=True
    )

    await run_build(
        interaction,
        template.value
    )


# ============================================================
# GERADOR DE SITES
# ============================================================

class SiteSelect(discord.ui.Select):

    def __init__(self, user_id: int):

        options = [
            discord.SelectOption(
                label=data["titulo"],
                value=key,
                emoji=data["emoji"],
                description=data["tagline"][:100]
            )
            for key, data in sitegen.TIPOS.items()
        ]

        super().__init__(
            placeholder="🌐 Escolha o tipo de site...",
            options=options
        )

        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):

        tipo = self.values[0]
        data = sitegen.TIPOS[tipo]

        class NomeModal(discord.ui.Modal, title="Nome do seu site"):

            nome = discord.ui.TextInput(
                label="Nome/título do site",
                placeholder=data["titulo"],
                required=False,
                max_length=60
            )

            async def on_submit(self, modal_interaction):

                nome = str(self.nome).strip() or None

                await modal_interaction.response.send_message(
                    embed=sitegen.site_embed(tipo, nome),
                    file=sitegen.site_file(tipo, nome)
                )

        await interaction.response.send_modal(NomeModal())


@bot.tree.command(
    name="site",
    description="🌐 Cria um site profissional pronto para usar"
)
async def site(interaction: discord.Interaction):

    view = discord.ui.View(timeout=120)
    view.add_item(SiteSelect(interaction.user.id))

    embed = discord.Embed(
        title="🌐 Gerador de Sites",
        description=(
            "Escolha o tipo de site no menu abaixo!\n\n"
            "✨ Crio sites modernos, responsivos e profissionais, "
            "com visual adaptado para celular e computador.\n\n"
            "📦 Você recebe um arquivo `.html` pronto para abrir "
            "e publicar."
        ),
        color=0x5865F2
    )

    await interaction.response.send_message(
        embed=embed,
        view=view
    )


# ============================================================
# COMANDO /LOGO
# ============================================================

@bot.tree.command(
    name="logo",
    description="🏷️ Mostra a identidade do Slayer Bot"
)
async def logo_cmd(interaction: discord.Interaction):

    embed = discord.Embed(
        title="⚔️ Slayer Bot",
        description=(
            "**Slayer** — seu assistente inteligente de criação!\n\n"
            "Monta servidores completos e cria sites profissionais "
            "com apenas alguns comandos.\n\n"
            f"✨ **{len(TEMPLATES)} modelos de servidor**\n"
            f"🌐 **{len(sitegen.TIPOS)} tipos de site**"
        ),
        color=0x5865F2
    )

    embed.set_image(
        url="attachment://slayer-logo.png"
    )

    embed.set_footer(
        text="Slayer Bot • identidade exclusiva"
    )

    await interaction.response.send_message(
        embed=embed,
        file=logo.logo_file()
    )


# ============================================================
# COMANDO /AJUDA
# ============================================================

@bot.tree.command(
    name="ajuda",
    description="❓ Mostra os comandos do Slayer Bot"
)
async def ajuda(interaction: discord.Interaction):

    embed = discord.Embed(
        title="⚔️ Slayer Bot — Central de Ajuda",
        description=(
            "Veja abaixo os comandos disponíveis.\n"
            "Você também pode me mencionar e escrever o que deseja!"
        ),
        color=0x5865F2
    )

    embed.add_field(
        name="🧩 Painel",
        value="`/painel` — abre o painel de criação.",
        inline=False
    )

    embed.add_field(
        name="🏗️ Criar servidor",
        value="`/criar` — cria uma estrutura profissional.",
        inline=False
    )

    embed.add_field(
        name="🌐 Criar site",
        value="`/site` — gera um site em HTML.",
        inline=False
    )

    embed.add_field(
        name="🏷️ Logo",
        value="`/logo` — mostra a identidade do bot.",
        inline=False
    )

    embed.add_field(
        name="🏓 Ping",
        value="`/ping` — mostra a latência.",
        inline=False
    )

    embed.add_field(
        name="📊 Servidor",
        value="`/servidor` — mostra informações do servidor.",
        inline=False
    )

    embed.add_field(
        name="🖼️ Avatar",
        value="`/avatar` — mostra o avatar de um usuário.",
        inline=False
    )

    embed.add_field(
        name="🧹 Limpar",
        value="`/limpar` — apaga mensagens.",
        inline=False
    )

    embed.add_field(
        name="💬 Inteligência artificial",
        value="Mencione o bot para fazer perguntas e conversar.",
        inline=False
    )

    embed.set_footer(
        text="Slayer Bot • Central de Ajuda"
    )

    await interaction.response.send_message(
        embed=embed
    )


# ============================================================
# COMANDO /PING
# ============================================================

@bot.tree.command(
    name="ping",
    description="🏓 Mostra a latência do bot"
)
async def ping(interaction: discord.Interaction):

    latency = round(bot.latency * 1000)

    await interaction.response.send_message(
        f"🏓 **Pong!** `{latency}ms` de latência."
    )


# ============================================================
# COMANDO /SERVIDOR
# ============================================================

@bot.tree.command(
    name="servidor",
    description="📊 Mostra informações deste servidor"
)
async def servidor(interaction: discord.Interaction):

    guild = interaction.guild

    if guild is None:
        return await interaction.response.send_message(
            "❌ Esse comando só funciona em servidores.",
            ephemeral=True
        )

    embed = discord.Embed(
        title=f"📊 {guild.name}",
        color=0x3498DB
    )

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    embed.add_field(
        name="👑 Dono",
        value=f"<@{guild.owner_id}>"
    )

    embed.add_field(
        name="👥 Membros",
        value=str(guild.member_count)
    )

    embed.add_field(
        name="📺 Canais",
        value=str(len(guild.channels))
    )

    embed.add_field(
        name="🗂️ Cargos",
        value=str(len(guild.roles))
    )

    embed.add_field(
        name="🆔 ID",
        value=str(guild.id)
    )

    embed.set_footer(
        text=f"Criado em {guild.created_at.strftime('%d/%m/%Y')}"
    )

    await interaction.response.send_message(
        embed=embed
    )


# ============================================================
# COMANDO /AVATAR
# ============================================================

@bot.tree.command(
    name="avatar",
    description="🖼️ Mostra o avatar de um usuário"
)
@app_commands.describe(
    usuario="De quem você quer ver o avatar"
)
async def avatar(
    interaction: discord.Interaction,
    usuario: discord.Member = None
):

    user = usuario or interaction.user

    embed = discord.Embed(
        title=f"🖼️ Avatar de {user.display_name}",
        color=0xE67E22
    )

    embed.set_image(
        url=user.display_avatar.url
    )

    await interaction.response.send_message(
        embed=embed
    )


# ============================================================
# COMANDO /LIMPAR
# ============================================================

@bot.tree.command(
    name="limpar",
    description="🧹 Apaga mensagens de um canal"
)
@app_commands.describe(
    quantidade="Quantidade de mensagens para apagar (1 a 100)"
)
async def limpar(
    interaction: discord.Interaction,
    quantidade: app_commands.Range[int, 1, 100] = 10
):

    if not interaction.user.guild_permissions.manage_messages:
        return await interaction.response.send_message(
            "❌ Você precisa da permissão **Gerenciar Mensagens**.",
            ephemeral=True
        )

    await interaction.response.defer(
        ephemeral=True
    )

    deleted = await interaction.channel.purge(
        limit=quantidade + 1
    )

    total = max(0, len(deleted) - 1)

    await interaction.followup.send(
        f"🧹 Apaguei **{total} mensagens**!",
        ephemeral=True
    )


# ============================================================
# SISTEMA DE MENÇÕES E INTELIGÊNCIA ARTIFICIAL
# ============================================================

@bot.event
async def on_message(message: discord.Message):

    if message.author.bot:
        return

    is_mention = (
        bot.user.mentioned_in(message)
        and not message.mention_everyone
    )

    is_reply_to_bot = (
        message.reference
        and isinstance(
            message.reference.resolved,
            discord.Message
        )
        and message.reference.resolved.author.id == bot.user.id
    )

    is_dm = isinstance(
        message.channel,
        discord.DMChannel
    )

    if is_mention or is_reply_to_bot or is_dm:
        await handle_mention(message)
        return

    await bot.process_commands(message)


async def handle_mention(message: discord.Message):

    async with message.channel.typing():

        content = (
            message.content
            .replace(f"<@{bot.user.id}>", "")
            .replace(f"<@!{bot.user.id}>", "")
            .strip()
            or "olá"
        )

        lowered = content.lower()

        # Painel por menção
        if "painel" in lowered or "dashboard" in lowered:

            if message.guild is None:
                return await message.reply(
                    "❌ O painel só pode ser aberto dentro de um servidor."
                )

            return await message.reply(
                embed=dashboard_embed(message.guild),
                view=Dashboard(message.author.id)
            )

        # Gerador de sites por menção
        tipo_site = sitegen.match_tipo(content)

        if tipo_site and any(
            word in lowered
            for word in (
                "site",
                "website",
                "página",
                "pagina",
                "web"
            )
        ):

            nome = None

            if "chamado" in lowered:
                nome = (
                    content.split("chamado")[-1]
                    .strip(" -.!?")
                    or None
                )

            return await message.reply(
                embed=sitegen.site_embed(tipo_site, nome),
                file=sitegen.site_file(tipo_site, nome)
            )

        # Interpretação de pedidos com IA
        try:
            intent = await ai.get_intent(
                content,
                str(message.author)
            )
        except Exception as e:
            print(f"[ERRO IA] {e}")

            return await message.reply(
                "❌ Tive um problema ao processar sua mensagem. "
                "Tente novamente."
            )

        if intent.get("action") == "build_server":

            if message.guild is None:
                return await message.reply(
                    "❌ Convide-me para um servidor primeiro!"
                )

            if not can_build(message.author):
                return await message.reply(
                    "❌ Você precisa da permissão "
                    "**Gerenciar Servidor** para criar estruturas."
                )

            template_key = intent.get(
                "template",
                "comunidade"
            )

            spec = (
                get_template(template_key)
                or intent.get("spec")
            )

            if not spec:
                return await message.reply(
                    "❌ Não consegui entender o modelo. "
                    "Tente: `@bot crie um servidor de futebol`"
                )

            await message.reply(
                "🚀 **Pedido entendido!** "
                "Vou começar a construir seu servidor. "
                "Os canais e cargos existentes serão preservados."
            )

            await run_build(
                message,
                template_key if get_template(template_key) else None,
                spec=spec
            )

        else:

            reply = intent.get(
                "reply",
                "🤖 Não entendi, mas pode pedir de outro jeito!"
            )

            chunks = [
                reply[i:i + 2000]
                for i in range(0, len(reply), 2000)
            ]

            for chunk in chunks:
                await message.reply(chunk)


# ============================================================
# INICIALIZAÇÃO
# ============================================================

if __name__ == "__main__":

    if not config.DISCORD_TOKEN:
        raise SystemExit(
            "❌ Defina DISCORD_TOKEN no arquivo .env "
            "(veja .env.example)"
        )

    bot.run(
        config.DISCORD_TOKEN
    )
