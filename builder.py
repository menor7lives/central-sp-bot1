
async def wipe_guild(guild, progress=None):
    """Remove canais, categorias e cargos antigos gerenciáveis."""

    bot_member = guild.me

    if bot_member is None:
        raise RuntimeError("Não consegui identificar o membro do bot.")

    bot_permissions = bot_member.guild_permissions

    if not bot_permissions.manage_channels:
        raise RuntimeError("O bot precisa da permissão Gerenciar Canais.")

    if not bot_permissions.manage_roles:
        raise RuntimeError("O bot precisa da permissão Gerenciar Cargos.")

    bot_top_role = bot_member.top_role

    wiped = {
        "channels": 0,
        "categories": 0,
        "roles": 0,
        "failed": 0,
    }

    channels = list(guild.channels)

    # Apaga canais primeiro e categorias por último.
    channels.sort(
        key=lambda channel: isinstance(
            channel, discord.CategoryChannel
        )
    )

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
            print(f"[RESET] Erro ao apagar {channel.name}: {error}")

        if progress and index % 5 == 0:
            try:
                await progress(
                    f"🧹 Limpando servidor: {index}/{total} canais..."
                )
            except Exception as error:
                print(f"[RESET] Erro ao atualizar progresso: {error}")

    # Remove cargos antigos que o bot consegue gerenciar.
    for role in list(guild.roles):

        if role.is_default() or role.managed:
            continue

        if role >= bot_top_role:
            continue

        try:
            await role.delete(
                reason="Slayer Bot — reconstrução autorizada"
            )

            wiped["roles"] += 1

        except (discord.Forbidden, discord.HTTPException) as error:
            wiped["failed"] += 1
            print(f"[RESET] Erro ao apagar cargo {role.name}: {error}")

    return wiped
