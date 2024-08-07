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
from routers.setting_profile import setting_profile_router
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
manager = ConnectionManager()

def get_token_from_cookie(cookie_string: str):
    cookies = cookie_string.split('; ')
    for cookie in cookies:
        name, value = cookie.split('=')
        if name == 'jwt':
            return value
    return None

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    cookie_string = await websocket.receive_text()
    token = get_token_from_cookie(cookie_string)
    if token:
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            await manager.connect(token, websocket)
            try:
                while True:
                    data = await websocket.receive_text()
                    await manager.broadcast(data)
            except WebSocketDisconnect:
                await manager.disconnect(token, websocket)
            except Exception as e:
                print(f"Error while receiving message: {e}")
                await manager.disconnect(token, websocket)
        except jwt.PyJWTError as e:
            print(f"JWT error: {e}")
            await websocket.close()
    else:
        print("No token provided, closing connection.")
        await websocket.close()