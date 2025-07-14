import asyncio
import random
import datetime
import numpy as np
import time
import uuid
from src.data.scripts.connection import get_connection
from src.modules.validator import (
    insert_valid_record,
    insert_audit_record,
    validate_device_data,
    update_device_stats
)
from broadcast import manager

# —— Configuración simulador ——  
N_SERVICES = 5
N_DEVICES_PER_SERVICE = 20
TOTAL_DEVICES = N_SERVICES * N_DEVICES_PER_SERVICE
INTERVAL_MINUTES = 15
INTERVAL_SECONDS = INTERVAL_MINUTES * 60
INTER_EVENT_MIN = 0.05
INTER_EVENT_MAX = 5
START_DATE = datetime.datetime(2025, 7, 7, 0, 0)

def get_last_accumulated(device_id: int) -> float:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT accumulated_value
          FROM audit_data
         WHERE device_id = ?
         ORDER BY timestamp DESC
         LIMIT 1
    """, (device_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0.0

def solar_profile(hour: int) -> float:
    if 6 <= hour <= 18:
        x = (hour - 6) / 12 * np.pi
        return np.sin(x)
    return 0.0

# Historial por dispositivo
device_history = {}

async def emit_record(device_id: int, sim_time: datetime.datetime, state: dict):
    value = round(state["accumulated_energy"], 2)
    timestamp = sim_time

    print(f"\n📤 Generado → Device {device_id} | Valor acumulado: {value} | Hora: {timestamp}")

    if device_id not in device_history:
        device_history[device_id] = []

    # Agrega a historial para validación
    device_history[device_id].append((device_id, timestamp, value))

    validated = validate_device_data(device_history[device_id])
    if not validated:
        print("⚠️ Aún no hay suficientes datos para validar.")
        return

    ts, val, delta, clas = validated[-1]
    record = {
        "id": str(uuid.uuid4().hex[:15]),
        "device_id": device_id,
        "delta_value": round(delta, 3),
        "accumulated_value": round(val, 3),
        "clasificacion": clas,
        "timestamp": ts.isoformat()
    }

    insert_audit_record(record)
    print(f"✅ Insertado en audit_data → Δ: {delta:.3f}, Clasificación: {clas}")

    if clas == "valido":
        insert_valid_record(record)
        print("🟢 Insertado en valid_records")

    update_device_stats(device_id, [delta])
    print("📊 Estadísticas actualizadas")

    await manager.broadcast({
        "type": "new_record",
        "device_id": device_id,
        "delta": delta,
        "accumulated": val,
        "clasificacion": clas,
        "timestamp": ts.isoformat()
    })


async def main():
    device_states = {
        device_id: {
            "accumulated_energy": get_last_accumulated(device_id),
            "frozen": False
        }
        for device_id in range(1, TOTAL_DEVICES + 1)
    }

    sim_time = datetime.datetime.combine(START_DATE, datetime.time(6, 0))

    while True:
        if sim_time.hour >= 18:
            sim_time = (sim_time + datetime.timedelta(days=1)).replace(
                hour=6, minute=0, second=0, microsecond=0
            )

        if 6 <= sim_time.hour <= 18:
            ids = list(device_states.keys())
            random.shuffle(ids)
            tick_start = time.monotonic()

            for device_id in ids:
                state = device_states[device_id]

                base_gen = solar_profile(sim_time.hour)
                delta = base_gen * random.uniform(0.5, 1.5)
                r = random.random()
                if r < 0.01:
                    delta = -random.uniform(0.1, 0.5)
                elif r < 0.02:
                    delta *= 8
                elif r < 0.04 and not state["frozen"]:
                    delta = 0
                    state["frozen"] = True
                else:
                    state["frozen"] = False

                # Actualiza acumulado
                state["accumulated_energy"] = max(
                    state["accumulated_energy"] + delta,
                    state["accumulated_energy"]
                )

                await emit_record(device_id, sim_time, state)
                await asyncio.sleep(random.uniform(INTER_EVENT_MIN, INTER_EVENT_MAX))

            elapsed = time.monotonic() - tick_start
            await asyncio.sleep(max(0, INTERVAL_SECONDS - elapsed))

        sim_time += datetime.timedelta(minutes=INTERVAL_MINUTES)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("⛔ Simulación detenida.")
