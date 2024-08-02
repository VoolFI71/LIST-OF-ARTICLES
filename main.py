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

app = FastAPI()

secret_key = "key"

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
    if cookie is None:
        pass
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM lists")
        rows = cursor.fetchall()
        respons = [row for row in rows]
        session = uuid4()
        cookie_value = str(f"{str(session)} , {str(int(time.time()))} , {str(int(time.time())+600)}").split(",")
    return {"Тексты": respons, "Cookie": cookie_value}

@app.post("/")
def create_list(list: model_list, request: Request):
    token = request.cookies.get("jwt")
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        with sqlite3.connect("db/database.db") as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO lists (nick, title, description) VALUES (?, ?, ?)", (payload["sub"], list.title, list.description))
            db.commit()
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="JWT token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid JWT token")

    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO lists (nick, title, description) VALUES (?, ?, ?)", (list.nick, list.title, list.description))
        db.commit()
    return {"message": "List created successfully"}

@app.get("/users", dependencies=[Depends(check_auth)])
def get_users():
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM logins")
        rows = cursor.fetchall()
    return rows

@app.get("/userss")
def get_users():
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM logins")
        rows = cursor.fetchall()
    return rows

@app.delete("/user/delete/{nick}")
def delete_user(nick: str):
    try:
        with sqlite3.connect("db/database.db") as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM logins WHERE nick=?", (nick,))
            db.commit()
            if cursor.rowcount == 0:  # Проверка, был ли удален хоть один элемент
                raise HTTPException(status_code=404, detail="User with {nick} not found")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Expense deleted successfully"}


@app.post("/user/register")
def create_user(user: Reg_User):
    if user.password!=user.password2:
        return {"message": "passwords are incorrect"}
    try:
        with sqlite3.connect("db/database.db") as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO logins (nick, password) VALUES (?, ?)", (user.nick, user.password))
            db.commit()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "User created successfully"}

@app.get("/user/login")
def login_user(user: model_user, response: Response):
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM logins WHERE nick=?", (user.nick,))
        rows = cursor.fetchall()

        if rows and rows[0][1]==user.password:
            token = jwt.encode({"sub": user.nick, "hash_password": user.password, "exp": int(time.time())+30}, secret_key, algorithm='HS256')
            response.set_cookie(key="jwt", value=token, httponly=True, secure=False)
            cursor.execute("UPDATE logins SET token=? WHERE nick=?", (token, user.nick))
            db.commit()
            return {"message": "You are logged in", "token": token}
        return {"message": "You are no logged"}
