import uuid
import sqlite3
import pandas as pd

DB = 'data/database.db'
CSV_SERV = 'data/historical/services.csv'
CSV_DEVS = 'data/historical/devices.csv'
CSV_RECS = 'data/historical/records.csv'

def load_table(table, df, cols):
    """Inserta todo el dataframe df en la tabla con columnas cols."""
    placeholders = ','.join('?' for _ in cols)
    sql = f"INSERT OR IGNORE INTO {table} ({','.join(cols)}) VALUES ({placeholders})"
    conn = sqlite3.connect(DB)
    conn.executemany(sql, df[cols].itertuples(index=False, name=None))
    conn.commit()
    conn.close()

    # 1. Carga services → projects
    df_s = pd.read_csv(CSV_SERV, names=['id','name'], header=0)
    load_table('projects', df_s, ['id','name'])

    # 2. Carga devices
    df_d = pd.read_csv(CSV_DEVS, names=['id','project_id'], header=0)
    load_table('devices', df_d, ['id','project_id'])

    # 3. Carga records → raw_records con UUID
    df_r = pd.read_csv(CSV_RECS, names=['device_id','timestamp','value'], header=0)
    df_r.insert(0, 'id', [str(uuid.uuid4().hex[:15]) for _ in range(len(df_r))])
    df_r['clasificacion'] = 'pendiente'
    load_table('raw_records', df_r, ['id','device_id','timestamp','value','clasificacion'])

    # 4. Validación rápida
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM projects");      print("Proyectos:",      cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM devices");       print("Dispositivos:",   cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM raw_records");   print("Registros total:", cur.fetchone()[0])
    conn.close()

