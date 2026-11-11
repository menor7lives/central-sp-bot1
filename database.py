"""Banco SQLite do Slayer Bot para XP, cargos por reação e estatísticas."""
import os, sqlite3, threading
from contextlib import contextmanager

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.getenv('SLAYER_DB_PATH', os.path.join(BASE, 'slayer.sqlite3'))
_LOCK = threading.RLock()
_INITIALIZED = False

@contextmanager
def _conn():
    con = sqlite3.connect(DB_PATH, timeout=30)
    con.execute("PRAGMA busy_timeout=30000")
    con.execute("PRAGMA foreign_keys=ON")
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

def init_db():
    global _INITIALIZED
    if _INITIALIZED:
        return
    os.makedirs(os.path.dirname(DB_PATH) or '.', exist_ok=True)
    with _LOCK, _conn() as con:
        con.execute("PRAGMA journal_mode=WAL")
        con.executescript('''
        CREATE TABLE IF NOT EXISTS xp (
          guild_id TEXT NOT NULL, user_id TEXT NOT NULL,
          xp INTEGER NOT NULL DEFAULT 0, level INTEGER NOT NULL DEFAULT 0,
          messages INTEGER NOT NULL DEFAULT 0, PRIMARY KEY(guild_id,user_id));
        CREATE TABLE IF NOT EXISTS reaction_roles (
          guild_id TEXT NOT NULL, message_id TEXT NOT NULL, emoji TEXT NOT NULL,
          role_id TEXT NOT NULL, PRIMARY KEY(guild_id,message_id,emoji));
        CREATE TABLE IF NOT EXISTS stats (
          guild_id TEXT NOT NULL, key TEXT NOT NULL, value INTEGER NOT NULL DEFAULT 0,
          PRIMARY KEY(guild_id,key));
        ''')
    _INITIALIZED = True

def add_xp(guild_id, user_id, amount):
    init_db()
    with _LOCK, _conn() as con:
        con.execute('INSERT OR IGNORE INTO xp(guild_id,user_id) VALUES(?,?)',(str(guild_id),str(user_id)))
        row=con.execute('SELECT xp,level,messages FROM xp WHERE guild_id=? AND user_id=?',(str(guild_id),str(user_id))).fetchone()
        total=row['xp']+int(amount); level=int(total**0.5//5)
        con.execute('UPDATE xp SET xp=?,level=?,messages=messages+1 WHERE guild_id=? AND user_id=?',(total,level,str(guild_id),str(user_id)))
        return {'xp':total,'level':level,'messages':row['messages']+1,'leveled_up':level>row['level']}

def get_xp(guild_id,user_id):
    init_db()
    with _conn() as con:
        row=con.execute('SELECT xp,level,messages FROM xp WHERE guild_id=? AND user_id=?',(str(guild_id),str(user_id))).fetchone()
        return dict(row) if row else {'xp':0,'level':0,'messages':0}

def top_xp(guild_id,limit=10):
    init_db()
    with _conn() as con:
        return [dict(r) for r in con.execute('SELECT user_id,xp,level,messages FROM xp WHERE guild_id=? ORDER BY xp DESC LIMIT ?', (str(guild_id),int(limit))).fetchall()]

def save_reaction_role(guild_id,message_id,emoji,role_id):
    init_db()
    with _LOCK, _conn() as con:
        con.execute('INSERT OR REPLACE INTO reaction_roles VALUES(?,?,?,?)',(str(guild_id),str(message_id),str(emoji),str(role_id)))

def get_reaction_role(guild_id,message_id,emoji):
    init_db()
    with _conn() as con:
        r=con.execute('SELECT role_id FROM reaction_roles WHERE guild_id=? AND message_id=? AND emoji=?',(str(guild_id),str(message_id),str(emoji))).fetchone()
        return int(r['role_id']) if r else None
