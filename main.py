import json
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi import Path
from pydantic import BaseModel
from fastapi.responses import FileResponse
import uvicorn
from fastapi import FastAPI, Cookie, Request, Response, Depends, WebSocketDisconnect
from fastapi import Body, Header, WebSocket
from fastapi import HTTPException
from routers.auth import router_auth
from routers.delete_user import router_delete_user
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers.login import router_login
from routers.register import router_reg
from routers.profile import router_profile
from routers.users import router_users
from routers.lists import router_lists
from config import secret_key, check_token, check_token_ws, ConnectionManager, ChatManager
from routers.main_page import main_page_router as router_main_page
from routers.setting_profile import setting_profile_router
from routers.poop import pop
import os, redis, aiosqlite
from pydantic_models import Message
import time
from db.models import metadata_chat, metadata_logins, metadata_lists
from db.database2 import engine
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
app.include_router(setting_profile_router)
app.include_router(pop)

manager_users = ConnectionManager()
manager_chat = ChatManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connection_closed = False
    try:
        token = await websocket.receive_text()  # Получаем токен из сообщения
        nick = await check_token_ws(token)  # Проверяем токен
        if nick:
            await manager_users.connect(nick, websocket)
            while True:
                data = await websocket.receive_text()
                await manager_users.broadcast(data)
        else:
            print("Токен не предоставлен, закрываем соединение.")
            await websocket.close()

    except WebSocketDisconnect:
        if not connection_closed:
            await manager_users.disconnect(nick, websocket)
            connection_closed = True
    except Exception as e:
        print(f"Ошибка при получении сообщения: {e}")
        if not connection_closed:
            await manager_users.disconnect(nick, websocket)
            connection_closed = True

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    await manager_chat.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager_chat.broadcast(data)
    except WebSocketDisconnect:
        await manager_chat.disconnect(websocket)
        await websocket.close()
    except Exception as e:
        await websocket.close()
        print(f"Ошибка: {e}")

#metadata_chat.drop_all(engine)
metadata_chat.create_all(engine)
#metadata_lists.drop_all(engine)
metadata_lists.create_all(engine)
#metadata_logins.drop_all(engine)
metadata_logins.create_all(engine)