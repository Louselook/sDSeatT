# Simulador - Dispositivos Solares - Ejercicio Técnico

## Configuración del Entorno Virtual

### 1. Crear un entorno virtual

Usamos `venv` para crear un entorno aislado que nos permitirá gestionar las dependencias del proyecto:

```bash
python -m venv venv
````

### 2. Activar el entorno virtual

Dependiendo de tu sistema operativo:

#### En Windows:

```bash
venv\Scripts\activate
```

#### En Linux / macOS:

```bash
source venv/bin/activate
```

---

## Instalar las dependencias

Con el entorno virtual activo, instala los paquetes necesarios desde el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Ejecutar el generador de datos históricos y entrenamiento inicial

Este comando inicializa el sistema generando datos históricos simulados durante los últimos **7 días**. A partir de ellos, el sistema:

* pobla los modelos
* Mapea y define comportamientos típicos.
* Construye una base estadística para futuras predicciones.
* Pondra en marcha el servidor.

### Ejecutar:

```bash
py main.py
```

---

## Ejecutar simulación de nuevos datos (vía Swagger UI)

Una vez generado el historial y ajustado el sistema, puedes simular nuevos datos los cuales seran clasificados segun si detecta o no comportamientos atípicos.

### 1. Abre Swagger UI:

```
http://localhost:8000/docs
```

### 3. Ejecutar simulación:

Usa el endpoint:

```
POST /iniciar_simulacion
```

Haz clic en **"Try it out"** → **"Execute"** para iniciar la simulación de datos nuevos.

---

---

## Pruebas con datos atípicos (errores intencionados) ❌

```bash
simulator_mistake.py
```
Este simulador genera exclusivamente **datos incorrectos o atípicos**, como:

### Ejecución

> Si ya tienes el servidor en marcha (`uvicorn`, FastAPI, etc.), **abre una nueva terminal** y ejecuta:

```bash
py simulator_mistake.py
```

Esto iniciará la simulación de errores de forma paralela al sistema principal. Los datos serán enviados, validados y registrados como cualquier otro, permitiendo probar el comportamiento ante anomalías.

---

## 🔧 Personalización de los simuladores

Los archivos `simulator.py` (normal) y `simulator_mistake.py` (errores) se encuentran en la raíz del proyecto.

Puedes modificar variables al inicio de cada archivo para ajustar el comportamiento de la simulación:

```python
N_SERVICES = 5                      # Número de servicios simulados
N_DEVICES_PER_SERVICE = 20         # Dispositivos por servicio
TOTAL_DEVICES = N_SERVICES * N_DEVICES_PER_SERVICE

INTERVAL_MINUTES = 15              # Intervalo entre cada ciclo de simulación
INTERVAL_SECONDS = INTERVAL_MINUTES * 60

INTER_EVENT_MIN = 0.5              # Tiempo mínimo entre eventos por dispositivo
INTER_EVENT_MAX = 3                # Tiempo máximo entre eventos por dispositivo

START_DATE = datetime.datetime(2025, 7, 7, 0, 0)  # Fecha de inicio de la simulación
```
