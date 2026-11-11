
import os
import discord

def logo_file():
    logo_path = os.path.join(
        os.path.dirname(__file__),
        "slayer-logo.png"
    )

    if not os.path.isfile(logo_path):
        raise FileNotFoundError(
            f"Logo não encontrada: {logo_path}"
        )

    return discord.File(
        logo_path,
        filename="slayer-logo.png"
    )
