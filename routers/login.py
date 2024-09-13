from fastapi import APIRouter, HTTPException, Response
import sqlite3
import jwt
import time
from config import secret_key
from fastapi.templating import Jinja2Templates
from fastapi import Request, Form, Depends
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse, RedirectResponse
from routers.auth import hash_password
from config import check_token
import aiosqlite

router_login = APIRouter()

templates = Jinja2Templates(directory="front/templates")

@router_login.get("/user/login", response_class=HTMLResponse)
async def page_login_user(request: Request, response: Response, nick: str = Depends(check_token)):
    if nick is None:
        return templates.TemplateResponse("login.html", {"request": request})
    return RedirectResponse(url="/", status_code=302)

@router_login.post("/user/login")
async def login_user(response: Response, request: Request, nick: str = Form(...), password: str = Form(...)):
    async with aiosqlite.connect("db/database.db") as db:
        async with db.execute("SELECT * FROM logins WHERE nick=?", (nick,)) as cursor:
            user = await cursor.fetchone()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        if user[1] != hash_password(password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        token = jwt.encode({"sub": nick, "exp": int(time.time()) + 300}, secret_key, algorithm='HS256')

        await db.execute("UPDATE logins SET token=? WHERE nick=?", (token, nick))
        await db.commit()

        return JSONResponse(content={"detail": "Login successful", "token": token})