"""Sistema de níveis e ranking por servidor."""
import database

def registrar_mensagem(guild_id, user_id):
    # 8–14 XP por mensagem; o cooldown é aplicado no evento do bot.
    import random
    return database.add_xp(guild_id, user_id, random.randint(8,14))

def rank(guild_id,user_id):
    return database.get_xp(guild_id,user_id)

def ranking(guild_id,limite=10):
    return database.top_xp(guild_id,limite)
