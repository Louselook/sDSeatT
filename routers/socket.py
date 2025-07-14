from fastapi import APIRouter, BackgroundTasks
from simulator import main as run_simulator

router = APIRouter(tags=["navigation"])

@router.post("/iniciar_simulacion")
async def iniciar_simulacion(background_tasks: BackgroundTasks):
    # Lanza la simulación en background sin bloquear al cliente
    background_tasks.add_task(run_simulator)
    return {"status": "Simulación iniciada"}
