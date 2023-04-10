from fastapi import WebSocket
from collections import defaultdict

class WebsocketManager:
    def __init__(self, logger):
        self.connections: dict = defaultdict(dict)
        self.logger = logger

    def connected_users(self, task_id):
        self.connections.get(task_id, None)

    async def connect(self, websocket: WebSocket, task_id: str):
        await websocket.accept()
        if task_id not in self.connections or len(self.connections[task_id]) == 0:
            self.connections[task_id] = []
        self.connections[task_id].append(websocket)
        self.logger.info(f"[WS] Connected to {task_id} : {len(self.connections[task_id])}")

    def remove(self, websocket: WebSocket, task_id: str):
        self.connections[task_id].remove(websocket)
        self.logger.info("User Disconnected!")
        self.logger.info(f"[WS] Remaining connection to {task_id}: {len(self.connections[task_id])}")

    async def broadcast_task_progress(self, message: str, task_id: str):
        if task_id in self.connections:
            for connection in self.connections[task_id]:
                await connection.send_text(message)