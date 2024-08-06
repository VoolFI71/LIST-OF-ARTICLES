import json
from typing import List
from fastapi.templating import Jinja2Templates
import uvicorn
from fastapi import FastAPI, Cookie, Request, Response, Depends, WebSocketDisconnect
from aiogram import *
from aiogram.types import *
from random import *
from fastapi import Body, Header, WebSocket
from fastapi import FastAPI, Body, HTTPException
from random import *
from uuid import uuid4
import jwt
from routers.auth import router_auth
from routers.delete_user import router_delete_user
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers.login import router_login
from routers.register import router_reg
from routers.profile import router_profile
from routers.users import router_users
from routers.lists import router_lists
from config import secret_key
from routers.main_page import main_page_router as router_main_page
from config import ConnectionManager

app = FastAPI()
templates = Jinja2Templates(directory="front/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="front/static"), name="static")

app.include_router(router_auth)
app.include_router(router_delete_user)
app.include_router(router_login)
app.include_router(router_reg)
app.include_router(router_profile)
app.include_router(router_users)
app.include_router(router_lists)
app.include_router(router_main_page)


manager = ConnectionManager()

def get_token_from_cookie(cookie_string: str):
    cookies = cookie_string.split('; ')
    for cookie in cookies:
        name, value = cookie.split('=')
        if name == 'jwt':
            return value
    return None

class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        self.active_connections.append(websocket)
        await websocket.accept()
        await self.broadcast_user_count()

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        await websocket.close()
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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    cookie_string = await websocket.receive_text()
    token = get_token_from_cookie(cookie_string)
    if token:
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            await manager.connect(websocket)
            try:
                while True:
                    data = await websocket.receive_text()
                    await manager.broadcast(data)
            except WebSocketDisconnect:
                await manager.disconnect(websocket)
            except Exception as e:
                print(f"Error while receiving message: {e}")
                await manager.disconnect(websocket)
        except jwt.PyJWTError as e:
            print(f"JWT error: {e}")
            await websocket.close()
    else:
        print("No token provided, closing connection.")
        await websocket.close() 