import json
from typing import List
import jwt
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
        self.active_connections: list[WebSocket] = []
        self.active_nicks2: dict[str, int] = {}

    async def connect(self, token: str, websocket: WebSocket):
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        self.active_connections.append(websocket)
        if payload["sub"] not in self.active_nicks2:
            self.active_nicks2[payload["sub"]] = 0
        self.active_nicks2[payload["sub"]] += 1
        await self.broadcast_user_count()

    async def disconnect(self, token, websocket: WebSocket):
        self.active_connections.remove(websocket)
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        if payload["sub"] in self.active_nicks2:
            self.active_nicks2[payload["sub"]] -= 1
            if self.active_nicks2[payload["sub"]] == 0:
                del self.active_nicks2[payload["sub"]]
        await self.broadcast_user_count()

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, data: str):
        for connection in self.active_connections:
            await connection.send_text(data)

    async def broadcast_user_count(self):
        count2 = [1 for count_name in self.active_nicks2 if self.active_nicks2[count_name] >= 1]
        print(count2)
        message = json.dumps({"user_count": len(count2)})
        await self.broadcast(message)