from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect
from .database import ws_manager, analytics_data

router = APIRouter()

@router.websocket("/ws/analytics")
async def analytics_websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket, "analytics")
    await analytics_data()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Data received from client: {data}")
            room_members = (
                ws_manager.connected_users("analytics")
                if ws_manager.connected_users("analytics") is not None
                else []
            )
            if websocket not in room_members:
                # re-connect user
                await ws_manager.connect(websocket, "analytics")

            await ws_manager._notify(f"{data}", "analytics")
    except WebSocketDisconnect:
        ws_manager.remove(websocket, "analytics")
