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
router_auth = APIRouter()


templates = Jinja2Templates(directory="front/templates")

def check_token(token):
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM logins WHERE token=?", (token,))
        user = cursor.fetchone()
        if user is None:
            return False
    return True

def hash_password(password: str) -> str:
    sha256 = hashlib.sha256()

    sha256.update((password+salt).encode('utf-8'))

    hashed_password = sha256.hexdigest()

    return hashed_password

@router_auth.get("/user/register", response_class=HTMLResponse)
def create_user(request: Request):

    token = request.cookies.get("jwt")
    if not token:
        return templates.TemplateResponse("register.html", {"request": request})
    try:
        payload = jwt.decode(token.encode(), secret_key, algorithms=['HS256'])
    except:
        return templates.TemplateResponse("register.html", {"request": request})


@router_auth.post("/user/register")
def create_user(request: Request, response, Request, nick: str = Form(...), password: str = Form(...), password2: str = Form(...)):
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        hash_password = hash_password(password)
        cursor.execute("SELECT * FROM logins WHERE nick=?", (nick,))
        user = cursor.fetchone()
        if user is None:
            if password == password2:
                token = jwt.encode({"sub": nick, "exp": int(time.time()) + 10}, secret_key, algorithm='HS256')
                cursor.execute("INSERT INTO logins (nick, password, token) VALUES (?, ?, ?)", (nick, hash_password, token))
                db.commit()
                response.set_cookie(key="jwt", value=token, httponly=True, secure=False)
                return JSONResponse(content={"detail": "Register successful", "token": token})
            else:
                return JSONResponse(content={"detail": "Пароли не совпадают"}, status_code=400)
        else:
            return JSONResponse(content={"detail": "Пользователь с таким ником уже существует"}, status_code=400)

@router_auth.get("/user/login", response_class=HTMLResponse)
def page_login_user(request: Request, response: Response):
    token = request.cookies.get("jwt")
    if not token:
        return templates.TemplateResponse("login.html", {"request": request})
    try:
        payload = jwt.decode(token.encode(), secret_key, algorithms=['HS256'])
    except jwt.exceptions.ExpiredSignatureError:
         return templates.TemplateResponse("login.html", {"request": request})
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM logins WHERE token=?", (token,))
        user = cursor.fetchone()
        if user is None:
            return templates.TemplateResponse("login.html", {"request": request})
        else:
            return RedirectResponse(url="/users", status_code=302)

@router_auth.post("/user/login")
def login_user(response: Response, request: Request, nick: str = Form(...), password: str = Form(...)):
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM logins WHERE nick=?", (nick,))
        user = cursor.fetchone()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        if user[1] != hash_password(password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        token = jwt.encode({"sub": nick, "exp": int(time.time()) + 10}, secret_key, algorithm='HS256')
        response.set_cookie(key="jwt", value=token, httponly=True, secure=False)
        cursor.execute("UPDATE logins SET token=? WHERE nick=?", (token, nick))
        db.commit()
        return JSONResponse(content={"detail": "Login successful", "token": token})
