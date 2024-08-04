from fastapi import APIRouter, HTTPException, Response
from pydantic_models import Reg_User, User as model_user
import sqlite3
import jwt
import time
from config import secret_key, salt
import hashlib
from fastapi.templating import Jinja2Templates
from fastapi import Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse, RedirectResponse
from routers.auth import hash_password
router_reg= APIRouter()
templates = Jinja2Templates(directory="front/templates")


@router_reg.get("/user/register", response_class=HTMLResponse)
def create_user(request: Request):

    token = request.cookies.get("jwt")
    if not token:
        return templates.TemplateResponse("register.html", {"request": request})
    try:
        payload = jwt.decode(token.encode(), secret_key, algorithms=['HS256'])
        return RedirectResponse(url="/users", status_code=302)
    except:
        return templates.TemplateResponse("register.html", {"request": request})


@router_reg.post("/user/register")
def create_user(request: Request, response: Response, nick: str = Form(...), password: str = Form(...), password2: str = Form(...)):
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        h_password = hash_password(password)
        cursor.execute("SELECT * FROM logins WHERE nick=?", (nick,))
        existing_user = cursor.fetchone()
        if existing_user is None:
            if password == password2:
                if nick == "glebase":
                    token = jwt.encode({"sub": nick, "exp": int(time.time()) + 20, "role": "admin"}, secret_key, algorithm='HS256')
                    cursor.execute("INSERT INTO logins (nick, password, role, token) VALUES (?, ?, ?, ?)", (nick, h_password, "admin", token))
                    db.commit()
                else:
                    token = jwt.encode({"sub": nick, "exp": int(time.time()) + 20, "role": "user"}, secret_key, algorithm='HS256')
                    cursor.execute("INSERT INTO logins (nick, password, role, token) VALUES (?, ?, ?, ?)", (nick, h_password, "user", token))
                    db.commit()
                return JSONResponse(content={"detail": "Register successful", "token": token})
            else:
                return JSONResponse(content={"detail": "Пароли не совпадают"}, status_code=400)
        else:
            return JSONResponse(content={"detail": "Пользователь с таким ником уже существует"}, status_code=401)
