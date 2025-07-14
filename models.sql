-- Proyectos
CREATE TABLE IF NOT EXISTS projects (
  id   INTEGER PRIMARY KEY,
  name TEXT    NOT NULL UNIQUE
);

-- Dispositivos: con estadísticas de deltas
CREATE TABLE IF NOT EXISTS devices (
  id            INTEGER PRIMARY KEY,
  project_id    INTEGER NOT NULL REFERENCES projects(id),
  mean_delta    REAL    NOT NULL DEFAULT 0.0,
  std_delta     REAL    NOT NULL DEFAULT 0.0,
  var_delta     REAL    NOT NULL DEFAULT 0.0
);

-- Registros auditados (todos: válidos, inciertos, cuarentena)
CREATE TABLE IF NOT EXISTS audit_data (
  id                  TEXT    PRIMARY KEY,
  device_id           INTEGER NOT NULL REFERENCES devices(id),
  delta_value         REAL    NOT NULL,   -- lo que "genera" en ese intervalo
  accumulated_value   REAL    NOT NULL,   -- generación total acumulada hasta timestamp
  clasificacion       TEXT    CHECK(clasificacion IN ('valido','incierto','cuarentena')),
  timestamp           TEXT    NOT NULL
);

-- Registros válidos únicamente (nueva tabla)
CREATE TABLE IF NOT EXISTS valid_records (
  id                  TEXT    PRIMARY KEY,
  device_id           INTEGER NOT NULL REFERENCES devices(id),
  delta_value         REAL    NOT NULL,   -- lo que "genera" en ese intervalo
  accumulated_value   REAL    NOT NULL,   -- generación total acumulada hasta timestamp
  timestamp           TEXT    NOT NULL
);

-- Índices para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_audit_device_timestamp ON audit_data(device_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_valid_device_timestamp ON valid_records(device_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_clasificacion ON audit_data(clasificacion);