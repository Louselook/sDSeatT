from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from broadcast import manager
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from routers.api import router as api_router
from routers.navigation import router as nav_router
from routers.socket import router as sim_router

app = FastAPI(title="Backend Erco", version="1.0.0")

app.include_router(api_router)
app.include_router(nav_router)
app.include_router(sim_router)

# 3) Servimos estáticos y templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws/updates")
async def websocket_updates(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            # Si quieres mantener viva la conexión, espera algo (ping/pong)
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(ws)