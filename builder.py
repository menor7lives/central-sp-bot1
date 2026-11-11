
"""Slayer Bot — construção e reconstrução de servidores."""

import discord


# Permissões permitidas para cargos.
VALID_ROLE_PERMISSIONS = {
    "manage_guild",
    "manage_channels",
    "manage_roles",
    "manage_messages",
    "kick_members",
    "ban_members",
    "view_channel",
    "send_messages",
    "read_message_history",
    "attach_files",
    "embed_links",
    "add_reactions",
    "mention_everyone",
    "connect",
    "speak",
    "moderate_members",
    "move_members",
    "mute_members",
    "deafen_members",
    "use_application_commands",
}

# Permissões permitidas nas configurações de canais.
VALID_CHANNEL_PERMISSIONS = {
    "view_channel",
    "send_messages",
    "read_message_history",
    "attach_files",
    "embed_links",
    "add_reactions",
    "mention_everyone",
    "manage_messages",
    "manage_channels",
    "manage_roles",
    "connect",
    "speak",
    "stream",
    "use_voice_activation",
    "move_members",
    "mute_members",
    "deafen_members",
    "priority_speaker",
    "create_instant_invite",
    "send_tts_messages",
    "use_external_emojis",
    "use_external_stickers",
    "use_application_commands",
}


def _safe_color(value):
    try:
        color = int(value)
    except (TypeError, ValueError):
        color = 0x99AAB5

    return discord.Color(max(0, min(color, 0xFFFFFF)))


def _target(name, role_map, guild):
    if name == "@everyone":
        return guild.default_role

    return role_map.get(name)


def _overwrites(spec, role_map, guild):
    overwrites = {}

    if not isinstance(spec, dict):
        return overwrites

    for name, rules in spec.items():
        target = _target(name, role_map, guild)

        if target is None or not isinstance(rules, dict):
            continue

        overwrite = discord.PermissionOverwrite()

        allowed = rules.get("allow", [])
        denied = rules.get("deny", [])

        if not isinstance(allowed, list):
            allowed = []

        if not isinstance(denied, list):
            denied = []

        for permission in allowed:
            if permission in VALID_CHANNEL_PERMISSIONS:
                setattr(overwrite, permission, True)

        for permission in denied:
            if permission in VALID_CHANNEL_PERMISSIONS:
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
        raise RuntimeError(
            "Não consegui identificar o membro do bot."
        )

    bot_permissions = bot_member.guild_permissions

    if not bot_permissions.manage_channels:
        raise RuntimeError(
            "O bot precisa da permissão Gerenciar Canais."
        )

    if not bot_permissions.manage_roles:
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

    channels = list(guild.channels)

    # Categorias são apagadas por último.
    channels.sort(
        key=lambda channel: isinstance(
            channel, discord.CategoryChannel
        )
    )

    # Preserva o canal onde o comando foi executado.
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

        except (
            discord.Forbidden,
            discord.HTTPException
        ) as error:
            wiped["failed"] += 1

            print(
                f"[RESET] Erro ao apagar {channel.name}: {error}"
            )

        if progress and index % 5 == 0:
            await progress(
                f"🧹 Limpando servidor: {index}/{total} canais..."
            )

    # Remove somente cargos que o bot pode gerenciar.
    for role in list(guild.roles):
        if (
            role.is_default()
            or role.managed
            or role.permissions.administrator
        ):
            continue

        if role >= bot_top_role:
            continue

        try:
            await role.delete(
                reason="Slayer Bot — reconstrução autorizada"
            )

            wiped["roles"] += 1

        except (
            discord.Forbidden,
            discord.HTTPException
        ) as error:
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
    """Cria cargos, categorias e canais no servidor."""

    if not isinstance(spec, dict):
        raise ValueError(
            "A estrutura recebida pela IA é inválida."
        )

    wiped = {
        "channels": 0,
        "categories": 0,
        "roles": 0,
        "failed": 0,
    }

    if reset:
        if progress:
            await progress(
                "🧹 Limpando a estrutura antiga..."
            )

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

    roles_data = spec.get("roles", [])
    categories_data = spec.get("categories", [])

    if not isinstance(roles_data, list):
        roles_data = []

    if not isinstance(categories_data, list):
        categories_data = []

    # 1. Criação e configuração dos cargos.
    for role_data in roles_data:
        if not isinstance(role_data, dict):
            continue

        role_name = role_data.get("name")

        if not isinstance(role_name, str) or not role_name.strip():
            continue

        role = discord.utils.get(
            guild.roles,
            name=role_name
        )

        permissions = discord.Permissions()

        role_permissions = role_data.get("permissions", [])

        if not isinstance(role_permissions, list):
            role_permissions = []

        for permission in role_permissions:
            if permission in VALID_ROLE_PERMISSIONS:
                setattr(permissions, permission, True)

        color = _safe_color(
            role_data.get("color", 0x99AAB5)
        )

        hoist = bool(role_data.get("hoist", False))

        if role is None:
            role = await guild.create_role(
                name=role_name,
                permissions=permissions,
                color=color,
                hoist=hoist,
                mentionable=True,
                reason="Slayer Bot — criação automática",
            )

            created["roles"] += 1

        elif not role.managed and role < guild.me.top_role:
            await role.edit(
                permissions=permissions,
                color=color,
                hoist=hoist,
                mentionable=True,
                reason="Slayer Bot — atualização automática",
            )

        role_map[role_name] = role

    # 2. Criação das categorias e dos canais.
    for category_data in categories_data:
        if not isinstance(category_data, dict):
            continue

        category_name = category_data.get("name")

        if (
            not isinstance(category_name, str)
            or not category_name.strip()
        ):
            continue

        overwrites = _overwrites(
            category_data.get("overwrites"),
            role_map,
            guild
        )

        category = discord.utils.get(
            guild.categories,
            name=category_name
        )

        if category is None:
            category = await guild.create_category(
                category_name,
                overwrites=overwrites,
                reason="Slayer Bot — criação automática",
            )

            created["categories"] += 1

        else:
            await category.edit(
                overwrites=overwrites
            )

        channels_data = category_data.get("channels", [])

        if not isinstance(channels_data, list):
            channels_data = []

        for channel_data in channels_data:
            if not isinstance(channel_data, dict):
                continue

            name = channel_data.get("name")

            if not isinstance(name, str) or not name.strip():
                continue

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
                    user_limit = channel_data.get("user_limit")

                    if user_limit is not None:
                        try:
                            user_limit = max(
                                0,
                                min(int(user_limit), 99)
                            )
                        except (TypeError, ValueError):
                            user_limit = None

                    await guild.create_voice_channel(
                        name,
                        category=category,
                        overwrites=channel_overwrites,
                        user_limit=user_limit,
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
                f"✅ Categoria **{category_name}** configurada."
            )

    created["wiped"] = wiped

    return created


def summary_embed(
    spec,
    created,
    template_label=None,
    wiped=None
):
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
