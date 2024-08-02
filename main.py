import requests
import time
import os
import uvicorn
import asyncio
import jwt
import sqlalchemy
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, UUID4
from fastapi import FastAPI, Cookie, Response, HTTPException, Request, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
from aiogram import *
from aiogram.types import *
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import ContentType
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F
from aiogram.filters import BaseFilter
from random import *
from secrets import token_urlsafe
from sqlalchemy import create_engine, text
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean
from fastapi import Body, Header
from fastapi import FastAPI, Body, HTTPException
from fastapi.responses import RedirectResponse
from random import *
import sqlite3
from pydantic_models import User as model_user
from pydantic_models import List as model_list
from pydantic_models import Reg_User
import json
from uuid import uuid4
import jwt
from routers.auth import router_auth
from routers.delete_user import router_delete_user
from config import secret_key
app = FastAPI()

def check_auth(request: Request):
    token = request.cookies.get("jwt")
    if not token :
        raise HTTPException(status_code=403, detail="Аунтефикация не пройдена")  # Если токена нет, возвращаем 403
    try:
        # Попытка декодировать токен
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload  # Если декодирование успешно, возвращаем полезную нагрузку (payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="JWT token has expired")  # Если токен просрочен
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid JWT token")  # Если токен недействителен

@app.get("/")
def get_lists(response: Response, cookie: str=Cookie(None)):
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM lists")
        rows = cursor.fetchall()
        respons = [row for row in rows]
        session = uuid4()
        cookie_value = str(f"{str(session)} , {str(int(time.time()))} , {str(int(time.time())+600)}").split(",")
    return {"Тексты": respons, "Cookie": cookie_value}

@app.post("/create/list")
def page_of_create_list(list: model_list, request: Request):
    token = request.cookies.get("jwt")
    if not token:
        return RedirectResponse(url="/user/login", status_code=302)
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        with sqlite3.connect("db/database.db") as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO lists (nick, title, description) VALUES (?, ?, ?)", (payload["sub"], list.title, list.description))
            db.commit()
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="JWT токен больше не работает, зайдите в аккаунт заново")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid JWT token")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Ошибка в базе данных: {str(e)}")
    return {"message": "List created successfully"}

@app.get("/users", dependencies=[Depends(check_auth)])
def get_users():
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM logins")
        rows = cursor.fetchall()
    return rows

@app.get("/admin/users")
def get_users():
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM logins")
        rows = cursor.fetchall()
    return rows

app.include_router(router_auth)
app.include_router(router_delete_user)