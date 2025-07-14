# src/alerts.py
from broadcast import manager
from datetime import datetime

# Estado en memoria
device_hist = {}  # device_id → {last_three, last_change_ts, last_acc}

async def check_alerts(record: dict):
    sid = record["device_id"]
    h = device_hist.setdefault(sid, {
        "last_three": [],
        "last_change": datetime.fromisoformat(record["timestamp"]),
        "last_acc": record["accumulated_value"]
    })

    # Actualizar histórico de últimos 3
    h["last_three"].append(record["clasificacion"])
    if len(h["last_three"]) > 3:
        h["last_three"].pop(0)

    # Alerta 1: 3x cuarentena
    if all(c == "cuarentena" for c in h["last_three"]):
        await manager.broadcast({ "type": "alert", "message": f"Dispositivo {sid}: 3 registros en cuarentena" })

    # Alerta 2: delta negativo
    if record["delta_value"] < 0:
        await manager.broadcast({ "type": "alert", "message": f"Dispositivo {sid}: delta negativo" })

    # Alerta 3: sin cambio > 1 h
    now = datetime.fromisoformat(record["timestamp"])
    if record["accumulated_value"] != h["last_acc"]:
        h["last_change"] = now
        h["last_acc"] = record["accumulated_value"]
    else:
        if (now - h["last_change"]).total_seconds() >= 3600:
            await manager.broadcast({ "type": "alert", "message": f"Dispositivo {sid}: sin cambio > 1 h" })
