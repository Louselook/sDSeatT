from src.data.scripts.connection import get_connection

def load_table(table, df, cols):
    """Inserta todo el dataframe df en la tabla con columnas cols."""
    placeholders = ','.join('?' for _ in cols)
    sql = f"INSERT OR IGNORE INTO {table} ({','.join(cols)}) VALUES ({placeholders})"
    conn = get_connection()
    conn.executemany(sql, df[cols].itertuples(index=False, name=None))
    conn.commit()
    conn.close()