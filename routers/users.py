
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, UUID4
from fastapi import APIRouter, FastAPI, Cookie, Response, HTTPException, Request, Depends, WebSocketDisconnect, status
from aiogram.filters import BaseFilter
from random import *
from fastapi import FastAPI, Body, HTTPException, WebSocket

from fastapi.responses import RedirectResponse
from random import *
import sqlite3
from uuid import uuid4
import jwt
from config import secret_key
from fastapi.responses import HTMLResponse


router_users = APIRouter()
templates = Jinja2Templates(directory="front/templates")

async def notify_users():
    for connection in active_users:
        # Отправляем обновление всем подключенным пользователям
        await connection.send_text(f"Active users: {', '.join(active_users)}")

@router_users.get("/users", response_class=HTMLResponse)
def get_users(request: Request, response: Response):
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM logins")
        rows = cursor.fetchall()
    token = request.cookies.get("jwt")
    if not token:
        pass
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return templates.TemplateResponse("users.html", {"request": request, "users": rows})
    except jwt.InvalidTokenError:
        return templates.TemplateResponse("users.html", {"request": request, "users": rows})
    return templates.TemplateResponse("users.html", {"request": request, "users": rows, "nick": payload["sub"]})

active_users = set()
active_connections = []

@router_users.websocket("/ws/users")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    token = websocket.cookies.get("jwt")
    username = None

    if token:
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            username = payload["sub"]
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            await websocket.close()
            return

    # Проверка на None перед добавлением
    if username:
        active_users.add(username)
        active_connections.append(websocket)
        await notify_active_users()  # Уведомляем о новом пользователе
        await websocket.send_text(f"Active users: {', '.join(active_users)}")
    try:
        while True:            await websocket.receive_text()
    except WebSocketDisconnect:
        if username:
            active_users.remove(username)
            active_connections.remove(websocket)
            await notify_active_users()


async def notify_active_users():
    user_list = list(active_users)
    message = f"Active users: {', '.join(user_list)}"

    for connection in active_connections:
        await connection.send_text(message)



@router_users.get("/admin/users")
def get_users():
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM logins")
        rows = cursor.fetchall()
    return rows