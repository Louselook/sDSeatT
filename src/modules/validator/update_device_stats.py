import statistics
from src.data.scripts.connection import get_connection

def update_device_stats(device_id, deltas):
    """
    Actualiza las estadísticas de un dispositivo en la tabla devices.
    """
    if not deltas:
        return

    valid_deltas = [d for d in deltas if d > 0]

    if valid_deltas:
        mean_delta = statistics.mean(valid_deltas)
        std_delta = statistics.stdev(valid_deltas) if len(valid_deltas) >= 2 else 0.0
        var_delta = statistics.variance(valid_deltas) if len(valid_deltas) >= 2 else 0.0
    else:
        mean_delta = std_delta = var_delta = 0.0

    mean_delta = round(mean_delta, 3)
    std_delta = round(std_delta, 3)
    var_delta = round(var_delta, 3)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE devices 
        SET mean_delta = ?, std_delta = ?, var_delta = ?
        WHERE id = ?
    """, (mean_delta, std_delta, var_delta, device_id))
    conn.commit()
    conn.close()
