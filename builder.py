
"""Slayer Bot — construção e reconstrução de servidores."""
import discord


def _target(name, role_map, guild):
    if name == "@everyone":
        return guild.default_role
    return role_map.get(name)


def _overwrites(spec, role_map, guild):
    overwrites = {}

    for name, rules in (spec or {}).items():
        target = _target(name, role_map, guild)
        if target is None:
            continue

        overwrite = discord.PermissionOverwrite()

        for permission in rules.get("allow", []):
            setattr(overwrite, permission, True)

        for permission in rules.get("deny", []):
            setattr(overwrite, permission, False)

        overwrites[target] = overwrite

    return overwrites


async def wipe_guild(
    guild,
    progress=None,
    preserve_channel_id=None
):
    """Remove canais, categorias e cargos que o bot pode gerenciar."""

    bot_member = guild.me

    if bot_member is None:
        raise RuntimeError("Não consegui identificar o membro do bot.")

    permissions = bot_member.guild_permissions

    if not permissions.manage_channels:
        raise RuntimeError(
            "O bot precisa da permissão Gerenciar Canais."
        )

    if not permissions.manage_roles:
        raise RuntimeError(
            "O bot precisa da permissão Gerenciar Cargos."
        )

    bot_top_role = bot_member.top_role

    wiped = {
        "channels": 0,
        "categories": 0,
        "roles": 0,
        "failed": 0,
    }

    # 1. Apagar canais antes das categorias.
    channels = [
        *guild.text_channels,
        *guild.voice_channels,
        *guild.stage_channels,
        *guild.forum_channels,
        *guild.categories,
    ]

    # Categorias ficam por último.
    channels.sort(
        key=lambda channel: isinstance(
            channel, discord.CategoryChannel
        )
    )

    # Preservar o canal onde o comando foi executado.
    if preserve_channel_id is not None:
        channels = [
            channel
            for channel in channels
            if channel.id != preserve_channel_id
        ]

    total = len(channels)

    for index, channel in enumerate(channels, start=1):
        try:
            is_category = isinstance(
                channel, discord.CategoryChannel
            )

            await channel.delete(
                reason="Slayer Bot — reconstrução autorizada"
            )

            if is_category:
                wiped["categories"] += 1
            else:
                wiped["channels"] += 1

        except (discord.Forbidden, discord.HTTPException) as error:
            wiped["failed"] += 1
            print(
                f"[RESET] Erro ao apagar {channel.name}: {error}"
            )

        if progress and index % 5 == 0:
            await progress(
                f"🧹 Limpando servidor: {index}/{total} canais..."
            )

    # 2. Apagar cargos que estão abaixo da hierarquia do bot.
    for role in list(guild.roles):
        if (
            role.is_default()
            or role.managed
            or role.permissions.administrator
        ):
            continue

        # Não remover o próprio cargo do bot nem cargos superiores.
        if role >= bot_top_role:
            continue

        try:
            await role.delete(
                reason="Slayer Bot — reconstrução autorizada"
            )
            wiped["roles"] += 1

        except (discord.Forbidden, discord.HTTPException) as error:
            wiped["failed"] += 1
            print(
                f"[RESET] Erro ao apagar cargo {role.name}: {error}"
            )

    return wiped


async def build_guild_structure(
    guild,
    spec,
    progress=None,
    reset=False,
    preserve_channel_id=None
):
    """Cria a estrutura do servidor."""

    wiped = {
        "channels": 0,
        "categories": 0,
        "roles": 0,
        "failed": 0,
    }

    if reset:
        if progress:
            await progress("🧹 Limpando a estrutura antiga...")

        wiped = await wipe_guild(
            guild,
            progress,
            preserve_channel_id=preserve_channel_id
        )

    role_map = {}

    created = {
        "roles": 0,
        "categories": 0,
        "channels": 0,
    }

    # 1. Criação dos cargos.
    for role_data in spec.get("roles", []):
        role = discord.utils.get(
            guild.roles,
            name=role_data["name"]
        )

        permissions = discord.Permissions()

        for permission in role_data.get("permissions", []):
            setattr(permissions, permission, True)

        if role is None:
            role = await guild.create_role(
                name=role_data["name"],
                permissions=permissions,
                color=discord.Color(
                    role_data.get("color", 0x99AAB5)
                ),
                hoist=role_data.get("hoist", False),
                mentionable=True,
                reason="Slayer Bot — criação automática",
            )
            created["roles"] += 1

        elif not role.managed and role < guild.me.top_role:
            await role.edit(
                permissions=permissions,
                color=discord.Color(
                    role_data.get("color", 0x99AAB5)
                ),
                hoist=role_data.get("hoist", False),
                mentionable=True,
                reason="Slayer Bot — atualização automática",
            )

        role_map[role_data["name"]] = role

    # 2. Categorias e canais.
    for category_data in spec.get("categories", []):
        overwrites = _overwrites(
            category_data.get("overwrites"),
            role_map,
            guild
        )

        category = discord.utils.get(
            guild.categories,
            name=category_data["name"]
        )

        if category is None:
            category = await guild.create_category(
                category_data["name"],
                overwrites=overwrites,
                reason="Slayer Bot — criação automática",
            )
            created["categories"] += 1
        else:
            await category.edit(overwrites=overwrites)

        for channel_data in category_data.get("channels", []):
            name = channel_data["name"]
            channel_type = channel_data.get("type", "text")

            channel_overwrites = _overwrites(
                channel_data.get("overwrites"),
                role_map,
                guild
            )

            if channel_type == "voice":
                channel = discord.utils.get(
                    guild.voice_channels,
                    name=name
                )

                if channel is None:
                    await guild.create_voice_channel(
                        name,
                        category=category,
                        overwrites=channel_overwrites,
                        user_limit=channel_data.get("user_limit"),
                        reason="Slayer Bot — criação automática",
                    )
                    created["channels"] += 1
                else:
                    await channel.edit(
                        category=category,
                        overwrites=channel_overwrites
                    )

            else:
                channel = discord.utils.get(
                    guild.text_channels,
                    name=name
                )

                if channel is None:
                    await guild.create_text_channel(
                        name,
                        category=category,
                        overwrites=channel_overwrites,
                        reason="Slayer Bot — criação automática",
                    )
                    created["channels"] += 1
                else:
                    await channel.edit(
                        category=category,
                        overwrites=channel_overwrites
                    )

        if progress:
            await progress(
                f"✅ Categoria **{category_data['name']}** configurada."
            )

    created["wiped"] = wiped
    return created


def summary_embed(spec, created, template_label=None, wiped=None):
    embed = discord.Embed(
        title="⚔️ Slayer Bot — Servidor configurado!",
        description=(
            f"**{spec.get('name', 'Servidor')}**"
            + (
                f" — modelo {template_label}"
                if template_label else ""
            )
        ),
        color=0x9B59B6,
    )

    if wiped:
        embed.add_field(
            name="🧹 Estrutura removida",
            value=(
                f"📺 Canais: {wiped['channels']}\n"
                f"📁 Categorias: {wiped['categories']}\n"
                f"👤 Cargos: {wiped['roles']}\n"
                f"⚠️ Falhas: {wiped['failed']}"
            ),
            inline=False,
        )

    embed.add_field(
        name="👤 Cargos criados",
        value=str(created["roles"])
    )

    embed.add_field(
        name="📁 Categorias criadas",
        value=str(created["categories"])
    )

    embed.add_field(
        name="📺 Canais criados",
        value=str(created["channels"])
    )

    embed.set_footer(
        text="Slayer Bot Premium • Reconstrução automática"
    )

    return embed
