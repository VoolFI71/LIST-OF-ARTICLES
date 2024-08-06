
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


@router_users.get("/admin/users")
def get_users():
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM logins")
        rows = cursor.fetchall()
    return rows