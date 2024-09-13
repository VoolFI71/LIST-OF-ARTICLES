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
from pydantic_models import List as model_list
from config import check_token
router_lists = APIRouter()

templates = Jinja2Templates(directory="front/templates")

@router_lists.get("/lists")
def get_lists(response: Response, request: Request, nick: str = Depends(check_token)):
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM lists")
        rows = cursor.fetchall()
        respons = [row for row in rows]
    if nick is None:
        return templates.TemplateResponse("lists.html", {"request": request, "response": respons})
    return templates.TemplateResponse("lists.html", {"request": request, "response": respons, "nick": nick})

@router_lists.get("/lists/{nick}")
def get_lists(response: Response, request: Request, nick: str = Depends(check_token)):
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM lists WHERE nick=?", (nick,))
        rows = cursor.fetchall()
        respons = [row for row in rows]
    if nick is None:
        return templates.TemplateResponse("user_lists.html", {"request": request, "response": respons})
    return templates.TemplateResponse("user_lists.html", {"request": request, "response": respons, "nick": nick})



@router_lists.get("/create/list")
def page_of_create_list(request: Request, nick: str = Depends(check_token)):
    if nick is None:
        return templates.TemplateResponse("create_lists.html", {"request": request})
    return templates.TemplateResponse("create_lists.html", {"request": request, "nick": nick})


@router_lists.post("/create/list")
def page_of_create_list(list: model_list, request: Request, nick: str = Depends(check_token)):
    if nick is None:
        raise HTTPException(status_code=401, detail=f"Сначала нужно войти в аккаунт: {str(e)}")
    try:        
        with sqlite3.connect("db/database.db") as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO lists (nick, title, description) VALUES (?, ?, ?)", (nick, list.title, list.description))
            db.commit()
            return JSONResponse(content={"detail": "Пост успешно создан"})
    except: 
        raise HTTPException(status_code=401, detail=f"Ошибка: {str(e)}")
