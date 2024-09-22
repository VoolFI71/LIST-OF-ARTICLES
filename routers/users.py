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
from db.database2 import engine
from db.database2 import ss
from sqlalchemy import text
router_users = APIRouter()
templates = Jinja2Templates(directory="front/templates")

@router_users.get("/users", response_class=HTMLResponse)
def get_users(request: Request, response: Response, nick: str = Depends(check_token)):
    with ss() as session:
        rows = session.execute(text("SELECT * FROM logins")).fetchall()
        messages = session.execute(text("SELECT * FROM chat ORDER BY id LIMIT 20")).fetchall()

    if nick is None:
        return templates.TemplateResponse("users.html", {"request": request, "messages": messages, "users": rows})
    return templates.TemplateResponse("users.html", {"request": request, "users": rows, "messages": messages, "nick": nick})

@router_users.get("/admin/users")
async def get_users():
    async with aiosqlite.connect("db/database.db") as db:
        async with db.execute("SELECT * FROM logins") as cursor:
            rows = await cursor.fetchall()
    return rows