"""Cargos automáticos por reação."""
import database

def registrar(guild_id,message_id,emoji,role_id):
    database.save_reaction_role(guild_id,message_id,emoji,role_id)

def cargo(guild_id,message_id,emoji):
    return database.get_reaction_role(guild_id,message_id,emoji)
