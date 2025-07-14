import asyncio
import random
import datetime
import numpy as np
import json
import time
from src.data.scripts.connection import get_connection

DB_FILE = 'src/data/scripts/database.db'

def get_last_accumulated(device_id: int) -> float:
    """
    Recupera el último accumulated_value de audit_data para ese device_id.
    Si no hay registros, retorna 0.0.
    """
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


# —— Configuración simulador ——  
N_SERVICES = 5
N_DEVICES_PER_SERVICE = 20
TOTAL_DEVICES = N_SERVICES * N_DEVICES_PER_SERVICE
INTERVAL_MINUTES = 15
INTERVAL_SECONDS = INTERVAL_MINUTES * 60
INTER_EVENT_MIN = 0.05
INTER_EVENT_MAX = 5
START_DATE = datetime.date(2025, 7, 1)

def solar_profile(hour: int) -> float:
    if 6 <= hour <= 18:
        x = (hour - 6) / 12 * np.pi
        return np.sin(x)
    return 0.0

async def emit_record(device_id: int, sim_time: datetime.datetime, state: dict):
    record = {
        "id_device": device_id,
        "timestamp": sim_time.isoformat(),
        "value": round(state["accumulated_energy"], 2)
    }
    # Aquí podrías además hacer un INSERT en audit_data...
    print(json.dumps(record))

async def main():
    # → Inicializo cada dispositivo con su último acumulado en DB
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

                # cálculo de delta y anomalías (igual que antes)
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

                # **Aquí actualizo el acumulado sobre lo que había en DB**
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
        print("Simulación detenida.")
