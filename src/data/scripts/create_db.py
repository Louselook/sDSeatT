import os
import sqlite3

def create_db():
    """Crea la base de datos y ejecuta el DDL desde el archivo SQL."""
    DB_FILE = 'src/data/db/database.db'
    SQL_FILE = 'models.sql'

    # 1) Eliminar antigua DB
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    # 2) Crear nueva DB y ejecutar el DDL
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        with open(SQL_FILE, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())