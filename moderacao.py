"""Sistema de advertências com histórico e punição automática."""
import time

import discord

import dados


def advertir(member, motivo: str, por_id: int) -> int:
    """Registra advertência e retorna o total do usuário."""
    g = dados.get(member.guild.id)
    lista = g["advertencias"].setdefault(str(member.id), [])
    lista.append({"motivo": (motivo or "sem motivo")[:200],
                  "por": por_id, "quando": int(time.time())})
    dados.salvar()
    return len(lista)


def lista(gid, uid) -> list:
    return dados.get(gid)["advertencias"].get(str(uid), [])


def limpar(gid, uid) -> int:
    g = dados.get(gid)
    n = len(g["advertencias"].pop(str(uid), []))
    if n:
        dados.salvar()
    return n


def deve_punir(total: int) -> bool:
    """A cada 3 advertências o usuário leva timeout automático."""
    return total > 0 and total % 3 == 0


def historico_embed(member, itens):
    e = discord.Embed(
        title=f"⚖️ Advertências de {member.display_name}",
        description=f"<@{member.id}> tem **{len(itens)}** advertência(s).",
        color=0xE67E22 if itens else 0x2ECC71)
    for i, it in enumerate(itens[-10:], start=1):
        quando = time.strftime("%d/%m/%Y %H:%M", time.localtime(it["quando"]))
        e.add_field(name=f"{i}• {quando}", value=f"{it['motivo']} — por <@{it['por']}>",
                    inline=False)
    if not itens:
        e.add_field(name="✨ Ficha limpa!", value="Nenhuma advertência registrada.", inline=False)
    e.set_footer(text="3 advertências = timeout automático de 10 minutos")
    return e
