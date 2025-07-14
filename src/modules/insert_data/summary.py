from src.data.scripts.connection import get_connection


def format_number(n: int) -> str:
    """Devuelve un entero con separador de miles."""
    return f"{n:,}"


def format_percentage(part: int, total: int) -> str:
    """Devuelve porcentaje con un decimal."""
    if total == 0:
        return "0.0%"
    return f"{part / total * 100:.1f}%"


def print_summary():
    conn = get_connection()
    cur = conn.cursor()

    # Conteos básicos
    cur.execute("SELECT COUNT(*) FROM projects")
    proyectos = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM devices")
    dispositivos = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM audit_data")
    totales = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM valid_records")
    validos = cur.fetchone()[0]

    # Distribución de clasificaciones
    cur.execute("SELECT COUNT(*) FROM audit_data WHERE clasificacion = 'valido'")
    cnt_val = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM audit_data WHERE clasificacion = 'incierto'")
    cnt_inc = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM audit_data WHERE clasificacion = 'cuarentena'")
    cnt_cua = cur.fetchone()[0]

    # Imprimir resumen
    print("=" * 50)
    print("📊 RESUMEN DE VALIDACIÓN")
    print("=" * 50)
    print(f"Proyectos:           {format_number(proyectos)}")
    print(f"Dispositivos:        {format_number(dispositivos)}")
    print(f"Registros totales:   {format_number(totales)}")
    print(f"Registros válidos:   {format_number(validos)}")

    print("\n📈 DISTRIBUCIÓN DE CLASIFICACIONES:")
    print(f"✅ Válidos:      {format_number(cnt_val)} ({format_percentage(cnt_val, totales)})")
    print(f"⚠️  Inciertos:    {format_number(cnt_inc)} ({format_percentage(cnt_inc, totales)})")
    print(f"❌ Cuarentena:   {format_number(cnt_cua)} ({format_percentage(cnt_cua, totales)})")

    # Estadísticas de dispositivos
    print("\n📱 ESTADÍSTICAS DE DISPOSITIVOS (primeros 5):")
    cur.execute(
        """
        SELECT id, mean_delta, std_delta, var_delta
        FROM devices
        WHERE mean_delta > 0
        ORDER BY id
        LIMIT 5
        """
    )
    rows = cur.fetchall()

    print(f"{'ID':<5}{'Media Δ':<12}{'Desv Δ':<12}{'Var Δ':<12}")
    print("-" * 45)
    for device_id, mean_d, std_d, var_d in rows:
        print(f"{device_id:<5}{mean_d:<12.4f}{std_d:<12.4f}{var_d:<12.4f}")

    conn.close()


if __name__ == '__main__':
    print_summary()
