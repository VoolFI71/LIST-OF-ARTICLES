import json, jwt, redis
from typing import List
from pydantic_models import Message
from fastapi import WebSocket, Request
secret_key = "key"
salt = "salt"

DATABASE="someDatabaseName"
DB_HOST="localhost"
DB_PORT = 5432
DB_USER= "dbUser"
DB_PASSWORD="1234"

redis_client = redis.Redis(host='localhost', port=6379, db=0)

async def check_token(request: Request):
    token = request.cookies.get("jwt")
    if not token:
        return None
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload["sub"]
    except jwt.PyJWTError:
        return None

async def check_token_ws(token: str):
    token = token[4:]
    if not token:
        return None
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        print("Токен истек.")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Неверный токен: {e}")
        return None

class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []
        self.active_nicks2: dict[str, int] = {}

    async def connect(self, nick: str, websocket: WebSocket):
        self.active_connections.append(websocket)
        if nick not in self.active_nicks2:
            self.active_nicks2[nick] = 0
        self.active_nicks2[nick] += 1
        await self.broadcast_user_count()

    async def disconnect(self, nick: str, websocket: WebSocket):
        self.active_connections.remove(websocket)
        if nick in self.active_nicks2:
            self.active_nicks2[nick] -= 1
            if self.active_nicks2[nick] == 0:
                del self.active_nicks2[nick]
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


class ChatManager():
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: Message):
        for connections in self.active_connections:
            await connections.send_text(message.message)