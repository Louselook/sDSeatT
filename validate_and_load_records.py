import pandas as pd
import uuid
from src.modules.insert_data import *
from src.modules.validator import *

CSV_SERV = 'src/data/db/services.csv'
CSV_DEVS = 'src/data/db/devices.csv'
CSV_RECS = 'src/data/db/records.csv'

def main():
    # 1. Carga services → projects
    print("📊 Cargando servicios...")
    df_s = pd.read_csv(CSV_SERV, names=['id','name'], header=0)
    load_table('projects', df_s, ['id','name'])

    # 2. Carga devices
    print("📱 Cargando dispositivos...")
    df_d = pd.read_csv(CSV_DEVS, names=['id','project_id'], header=0)
    load_table('devices', df_d, ['id','project_id'])

    # 3. Procesar y validar registros
    print("🔍 Procesando y validando registros...")
    df_r = pd.read_csv(CSV_RECS, names=['device_id','timestamp','value'], header=0)
    device_groups = df_r.groupby('device_id')

    audit_records = []
    valid_records = []
    total_validos = total_inciertos = total_cuarentena = 0

    print(f"📋 Validando {len(device_groups)} dispositivos...")
    for device_id, group in device_groups:
        device_records = [(row.device_id, row.timestamp, row.value) 
                          for _, row in group.iterrows()]

        validated = validate_device_data(device_records)
        if not validated:
            continue

        deltas = [rec[2] for rec in validated]
        update_device_stats(device_id, deltas)

        for timestamp, value, delta, clas in validated:
            audit_id = str(uuid.uuid4())
            d = dict(
                id=audit_id,
                device_id=device_id,
                delta_value=round(delta, 3),
                accumulated_value=round(value, 3),
                clasificacion=clas,
                timestamp=timestamp
            )
            audit_records.append(d)

            if clas == 'valido':
                valid_records.append({
                    **d,
                    'timestamp': timestamp  # valid_records no lleva 'clasificacion'
                })
                total_validos += 1
            elif clas == 'incierto':
                total_inciertos += 1
            else:
                total_cuarentena += 1

    # 4. Guardar audit_data y valid_records
    print("💾 Guardando registros auditados...")
    if audit_records:
        audit_df = pd.DataFrame(audit_records)
        load_table('audit_data', audit_df, [
            'id','device_id','delta_value','accumulated_value','clasificacion','timestamp'
        ])

    print("✅ Guardando registros válidos...")
    if valid_records:
        valid_df = pd.DataFrame(valid_records)
        load_table('valid_records', valid_df, [
            'id','device_id','delta_value','accumulated_value','timestamp'
        ])

    # 5. Mostrar resumen (delegado a summary.py)
    print_summary()

if __name__ == '__main__':
    main()
