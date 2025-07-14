import statistics

def validate_device_data(device_records):
    """
    Valida los datos de un dispositivo usando el algoritmo de deltas.
    Retorna una lista de tuplas (timestamp, value, delta, clasificacion)
    """
    if len(device_records) < 1:
        return []

    device_records = sorted(device_records, key=lambda x: x[1])
    validated_records = []
    deltas = []

    for idx, (device_id, timestamp, value) in enumerate(device_records):
        if idx == 0:
            delta = 0.0
            prev_value = value
        else:
            delta = value - prev_value
            prev_value = value

        deltas.append(delta)
        media = statistics.mean(deltas)
        desviacion = statistics.stdev(deltas) if len(deltas) >= 2 else 0.0

        lower_valido = media - desviacion
        upper_valido = media + desviacion

        if delta <= 0:
            clasificacion = "cuarentena"
        elif delta > media + 3 * desviacion:
            clasificacion = "cuarentena"
        elif not (lower_valido <= delta <= upper_valido):
            clasificacion = "incierto"
        else:
            clasificacion = "valido"

        validated_records.append((timestamp, value, delta, clasificacion))

    return validated_records
