import sqlite3

DB_FILE = 'src/data/db/database.db'

def get_connection():
    """
    Devuelve una conexión a la base de datos SQLite,
    con PRAGMA foreign_keys = ON para respetar las FKs.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
