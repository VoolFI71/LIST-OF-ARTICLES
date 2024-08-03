from fastapi import APIRouter, HTTPException, Response
from pydantic_models import Reg_User, User as model_user
import sqlite3
import jwt
import time
from config import secret_key, salt
import hashlib
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
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

@router_auth.post("/user/register")
def create_user(user: Reg_User):
    if user.password!=user.password2:
        return {"message": "passwords are incorrect"}
    try:
        with sqlite3.connect("db/database.db") as db:
            cursor = db.cursor()
            password = hash_password(user.password)
            cursor.execute("INSERT INTO logins (nick, password) VALUES (?, ?)", (user.nick, password))
            db.commit()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "User created successfully"}

templates = Jinja2Templates(directory="front/templates")

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
        token = jwt.encode({"sub": nick, "exp": int(time.time()) + 100}, secret_key, algorithm='HS256')
        response.set_cookie(key="jwt", value=token, httponly=True, secure=False)
        cursor.execute("UPDATE logins SET token=? WHERE nick=?", (token, nick))
        db.commit()
        return JSONResponse(content={"detail": "Login successful", "token": token})

@router_auth.get("/user/login", response_class=HTMLResponse)
def page_login_user(request: Request):
    token = request.cookies.get("jwt")
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM logins WHERE token=?", (token,))
        user = cursor.fetchone()
        if user is None:
            return templates.TemplateResponse("login.html", {"request": request})
        return templates.TemplateResponse("login.html", {"request": request})