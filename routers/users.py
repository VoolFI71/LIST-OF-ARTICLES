from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, UUID4
from fastapi import APIRouter, FastAPI, Cookie, Response, HTTPException, Request, Depends, WebSocketDisconnect, status
from aiogram.filters import BaseFilter
from random import *
from fastapi import FastAPI, Body, HTTPException, WebSocket, Depends
from fastapi.responses import RedirectResponse
from random import *
import sqlite3, jwt
from uuid import uuid4
from config import secret_key, check_token
from fastapi.responses import HTMLResponse
import aiosqlite

router_users = APIRouter()
templates = Jinja2Templates(directory="front/templates")

@router_users.get("/users", response_class=HTMLResponse)
async def get_users(request: Request, response: Response, nick: str = Depends(check_token)):
    async with aiosqlite.connect("db/database.db") as db:
        async with db.execute("SELECT * FROM logins") as cursor:
            rows = await cursor.fetchall()
    async with aiosqlite.connect("db/database.db") as db:
        async with db.execute("SELECT * FROM chat ORDER BY id LIMIT 20") as cursor:
            messages = await cursor.fetchall()
    if nick is None:
        return templates.TemplateResponse("users.html", {"request": request, "messages": messages, "users": rows})
    return templates.TemplateResponse("users.html", {"request": request, "users": rows, "messages": messages, "nick": nick})

@router_users.get("/admin/users")
async def get_users():
    async with aiosqlite.connect("db/database.db") as db:
        async with db.execute("SELECT * FROM logins") as cursor:
            rows = await cursor.fetchall()
    return rows