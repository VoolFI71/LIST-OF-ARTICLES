from fastapi import APIRouter, HTTPException, Response
from pydantic_models import Reg_User, User as model_user
import sqlite3
import jwt
import time
import shutil
import os
from config import secret_key, salt
import hashlib
from fastapi.templating import Jinja2Templates
from fastapi import Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from routers.auth import hash_password
from config import check_token
import aiosqlite
from db.database2 import engine
from db.database2 import ss
from sqlalchemy import text

router_reg= APIRouter()
templates = Jinja2Templates(directory="front/templates")

@router_reg.get("/user/register", response_class=HTMLResponse)
def create_user(request: Request, nick: str = Depends(check_token)):
    if nick is None:
        return templates.TemplateResponse("register.html", {"request": request})
    return RedirectResponse(url="/", status_code=302)


@router_reg.post("/user/register")
def create_user(
    request: Request, 
    response: Response, 
    nick: str = Form(...), 
    password: str = Form(...), 
    password2: str = Form(...)
):
    with ss() as session:
        h_password = hash_password(password)
        existing_user = session.execute(text("SELECT * FROM logins WHERE nick=:nick"), {"nick": nick}).scalar()
        if existing_user is None:
            if password == password2:
                role = "admin" if nick == "glebase" else "user"
                token = jwt.encode({"sub": nick, "exp": int(time.time()) + 300, "role": role}, secret_key, algorithm='HS256')
                session.execute(text("INSERT INTO logins (nick, password, role) VALUES (:nick, :password, :role)"), 
                            {"nick": nick, "password": h_password, "role": role})
                session.commit()
                image_path = os.path.abspath('default.png') # path to default image
                images_path = os.path.abspath('front/avatars') # path to new image
                name_file = str(nick) + ".png" #name of image
                new_images_path = os.path.join(images_path, name_file)
                shutil.copy2(image_path, new_images_path)
                return JSONResponse(content={"detail": "Register successful", "token": token})
            else:
                return JSONResponse(content={"detail": "Пароли не совпадают"}, status_code=400)
        else:
            return JSONResponse(content={"detail": "Пользователь с таким ником уже существует"}, status_code=401)
