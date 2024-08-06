import time
import uvicorn
import jwt
from pydantic import BaseModel, UUID4
from fastapi import APIRouter, FastAPI, Cookie, Response, HTTPException, Request, Depends, status
from aiogram import *
from aiogram.types import *
from random import *
from fastapi import Body, Header
from fastapi import FastAPI, Body, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from random import *
import sqlite3
from pydantic_models import List as model_list
from uuid import uuid4
import jwt
from routers.auth import router_auth
from routers.delete_user import router_delete_user
from config import secret_key
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from routers.auth import check_token
from pydantic_models import List as model_list
router_lists = APIRouter()

templates = Jinja2Templates(directory="front/templates")

@router_lists.get("/lists")
def get_lists(response: Response, request: Request):
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM lists")
        rows = cursor.fetchall()
        respons = [row for row in rows]
    token = request.cookies.get("jwt")
    if token:
        try:
            payload = jwt.decode(token.encode(), secret_key, algorithms=['HS256'])
            return templates.TemplateResponse("lists.html", {"request": request, "response": respons, "nick": payload["sub"]})
        except:
            return templates.TemplateResponse("lists.html", {"request": request, "response": respons})
    else:
        return templates.TemplateResponse("lists.html", {"request": request, "response": respons})

@router_lists.get("/lists/{nick}")
def get_lists(nick: str, response: Response, request: Request):
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM lists WHERE nick=?", (nick,))
        rows = cursor.fetchall()
        respons = [row for row in rows]
    token = request.cookies.get("jwt")
    if token:
        try:
            payload = jwt.decode(token.encode(), secret_key, algorithms=['HS256'])
            return templates.TemplateResponse("user_lists.html", {"request": request, "response": respons, "nick": payload["sub"]})
        except:
            return templates.TemplateResponse("user_lists.html", {"request": request, "response": respons})
    else:
        return templates.TemplateResponse("user_lists.html", {"request": request, "response": respons})


@router_lists.get("/create/list")
def page_of_create_list(request: Request):
    return templates.TemplateResponse("create_lists.html", {"request": request})

@router_lists.post("/create/list")
def page_of_create_list(list: model_list, request: Request):
    token = request.cookies.get("jwt")
    if not token or not(check_token(token)):
        return JSONResponse(content={"detail": "Сначала нужно войти в аккаунт"})
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        with sqlite3.connect("db/database.db") as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO lists (nick, title, description) VALUES (?, ?, ?)", (payload["sub"], list.title, list.description))
            db.commit()
            return JSONResponse(content={"detail": "Пост успешно создан"})
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="JWT токен больше не работает, зайдите в аккаунт заново")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid JWT token")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Ошибка в базе данных: {str(e)}")
