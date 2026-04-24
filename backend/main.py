from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

connected_clients: list[WebSocket] = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)


@app.post("/motion")
async def receive_motion(data: dict):
    message = json.dumps(data)
    disconnected = []
    notified = 0
    for client in connected_clients:
        try:
            await client.send_text(message)
            notified += 1
        except Exception:
            disconnected.append(client)
    for client in disconnected:
        connected_clients.remove(client)
    return {"status": "ok", "clients_notified": notified}
