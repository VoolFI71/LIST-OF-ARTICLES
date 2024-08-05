
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, UUID4
from fastapi import APIRouter, FastAPI, Cookie, Response, HTTPException, Request, Depends, status
from aiogram.filters import BaseFilter
from random import *
from fastapi import FastAPI, Body, HTTPException
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
    token = request.cookies.get("jwt")
    if not token:
        return RedirectResponse(url="/user/login", status_code=302)
    try:
        payload = jwt.decode(token.encode(), secret_key, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return RedirectResponse(url="/user/login", status_code=302)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid JWT token")
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM logins")
        rows = cursor.fetchall()
    return templates.TemplateResponse("users.html", {"request": request, "users": rows, "name": payload["sub"]})

@router_users.get("/admin/users")
def get_users():
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM logins")
        rows = cursor.fetchall()
    return rows