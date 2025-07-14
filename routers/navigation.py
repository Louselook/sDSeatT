from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["navigation"])

# Configura aquí la carpeta donde están tus templates
templates = Jinja2Templates(directory="templates")

@router.get("/projects/{project_id}", response_class=HTMLResponse)
async def project_detail(request: Request, project_id: int):
    """
    Ruta que sirve la página de detalle de un proyecto.
    El template `project.html` recibirá el request y el project_id.
    """
    return templates.TemplateResponse("project.html", {
        "request": request,
        "project_id": project_id
    })

@router.get("/dispositivo/{device_id}", response_class=HTMLResponse)
async def device_detail(request: Request, device_id: int):
    return templates.TemplateResponse("device.html", {
        "request": request,
        "device_id": device_id
    })

