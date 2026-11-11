
"""Slayer Bot — construção e reconstrução de servidores."""

import discord


BLOCKED_ROLE_PERMISSIONS = {
    "administrator",
    "manage_guild",
    "manage_channels",
    "manage_roles",
    "mention_everyone",
}


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
            if hasattr(overwrite, permission):
                setattr(overwrite, permission, True)

        for permission in rules.get("deny", []):
            if hasattr(overwrite, permission):
                setattr(overwrite, permission, False)

        overwrites[target] = overwrite

    return overwrites


async def wipe_guild(guild):
    """Remove canais, categorias e cargos não protegidos."""

    wiped = {"channels": 0, "roles": 0}
    bot_member = guild.me

    if bot_member is None:
        raise RuntimeError(
            "Não consegui identificar o membro do bot."
        )

    bot_top_role = bot_member.top_role

    # 1. Apaga canais comuns antes das categorias.
    channels = sorted(
        list(guild.channels),
        key=lambda channel: isinstance(
            channel, discord.CategoryChannel
        )
    )

    for channel in channels:
        try:
            await channel.delete(
                reason="Slayer Bot — reconstrução do servidor"
            )
            wiped["channels"] += 1

        except (discord.Forbidden, discord.HTTPException) as error:
            print(
                f"[RESET] Não foi possível apagar "
                f"{channel.name}: {error}"
            )

    # 2. Apaga apenas cargos gerenciáveis.
    for role in list(guild.roles):
        if role.is_default():
            continue

        if role.managed:
            continue

        if role >= bot_top_role:
            continue

        try:
            await role.delete(
                reason="Slayer Bot — reconstrução do servidor"
            )
            wiped["roles"] += 1

        except (discord.Forbidden, discord.HTTPException) as error:
            print(
                f"[RESET] Não foi possível apagar "
                f"{role.name}: {error}"
            )

    return wiped


async def build_guild_structure(
    guild,
    spec,
    progress=None,
    reset=False
):
    """Cria a estrutura do servidor, opcionalmente fazendo reset."""

    wiped = {"channels": 0, "roles": 0}

    if reset:
        if progress:
            await progress(
                "🧹 Limpando a estrutura antiga..."
            )

        wiped = await wipe_guild(guild)

    role_map = {}

    created = {
        "roles": 0,
        "categories": 0,
        "channels": 0,
    }

    # 1. Criação e configuração dos cargos.
    for role_data in spec.get("roles", []):
        role = discord.utils.get(
            guild.roles,
            name=role_data["name"]
        )

        permissions = discord.Permissions()

        for permission in role_data.get("permissions", []):
            if permission in BLOCKED_ROLE_PERMISSIONS:
                print(
                    f"[SEGURANÇA] Permissão bloqueada: {permission}"
                )
                continue

            if hasattr(permissions, permission):
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

        elif not role.permissions.administrator:
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
            await category.edit(
                overwrites=overwrites
            )

        # 3. Criação dos canais.
        for channel_data in category_data.get("channels", []):
            name = channel_data["name"]
            channel_type = channel_data.get("type", "text")

            channel = discord.utils.get(
                guild.channels,
                name=name
            )

            channel_overwrites = _overwrites(
                channel_data.get("overwrites"),
                role_map,
                guild
            )

            if channel is not None:
                if (
                    channel_type == "voice"
                    and isinstance(channel, discord.VoiceChannel)
                ):
                    await channel.edit(
                        category=category,
                        overwrites=channel_overwrites
                    )

                elif (
                    channel_type != "voice"
                    and isinstance(channel, discord.TextChannel)
                ):
                    await channel.edit(
                        category=category,
                        overwrites=channel_overwrites
                    )

                continue

            if channel_type == "voice":
                await guild.create_voice_channel(
                    name,
                    category=category,
                    overwrites=channel_overwrites,
                    user_limit=channel_data.get("user_limit"),
                    reason="Slayer Bot — criação automática",
                )

            else:
                await guild.create_text_channel(
                    name,
                    category=category,
                    overwrites=channel_overwrites,
                    reason="Slayer Bot — criação automática",
                )

            created["channels"] += 1

        if progress:
            await progress(
                f"✅ Categoria **{category_data['name']}** criada."
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
        title="✅ Servidor reconstruído!",
        description=(
            f"**{spec.get('name', 'Servidor')}**"
            + (
                f" — modelo {template_label}"
                if template_label else ""
            )
        ),
        color=0x2ECC71,
    )

    if wiped:
        embed.add_field(
            name="🧹 Estrutura removida",
            value=(
                f"{wiped['channels']} canais/categorias\n"
                f"{wiped['roles']} cargos"
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
        text="Slayer Bot • reconstrução automática"
    )

    return embed
