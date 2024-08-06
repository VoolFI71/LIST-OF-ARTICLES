import json
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi import WebSocket
secret_key = "key"
salt = "salt"

DATABASE="someDatabaseName"
DB_HOST="localhost"
DB_PORT = 5432
DB_USER= "dbUser"
DB_PASSWORD="1234"


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        self.active_connections.append(websocket)
        await self.broadcast_user_count()

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        await self.broadcast_user_count()

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, data: str):
        for connection in self.active_connections:
            await connection.send_text(data)

    async def broadcast_user_count(self):
        count = len(self.active_connections)
        message = json.dumps({"user_count": count})
        await self.broadcast(message)