import json
from typing import List
import jwt
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
        self.active_connections: dict[str, WebSocket] = []
        self.active_tokens: list[str] = []
    async def connect(self, token: str, websocket: WebSocket):
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        self.active_connections.append(websocket)
        self.active_tokens.append(payload["sub"])
        await self.broadcast_user_count()

    async def disconnect(self, token, websocket: WebSocket):
        self.active_connections.remove(websocket)
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        self.active_tokens.remove(payload["sub"])
        await self.broadcast_user_count()

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, data: str):
        for connection in self.active_connections:
            await connection.send_text(data)

    async def broadcast_user_count(self):
        count = len(set(self.active_tokens))
        message = json.dumps({"user_count": count})
        await self.broadcast(message)