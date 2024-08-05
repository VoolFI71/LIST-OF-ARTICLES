from fastapi import APIRouter, HTTPException, Response
import sqlite3
import jwt
import time
from config import secret_key
from fastapi.templating import Jinja2Templates
from fastapi import Request, Form
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse, RedirectResponse
from routers.auth import hash_password
router_login = APIRouter()
templates = Jinja2Templates(directory="front/templates")



@router_login.get("/user/login", response_class=HTMLResponse)
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

@router_login.post("/user/login")
def login_user(response: Response, request: Request, nick: str = Form(...), password: str = Form(...)):
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM logins WHERE nick=?", (nick,))
        user = cursor.fetchone()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        if user[1] != hash_password(password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        token = jwt.encode({"sub": nick, "exp": int(time.time()) + 30}, secret_key, algorithm='HS256')
        response.set_cookie(key="jwt", value=token, httponly=True, secure=False)
        cursor.execute("UPDATE logins SET token=? WHERE nick=?", (token, nick))
        db.commit()
        return JSONResponse(content={"detail": "Login successful", "token": token})