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

router_profile= APIRouter()
templates = Jinja2Templates(directory="front/templates")

@router_profile.get("/profile/{nick}")
def get_profile(nick: str, request: Request):
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM logins WHERE nick=?", (nick,))
        res = cursor.fetchone()
    if res is None:
        raise HTTPException(status_code=404, detail="User not found")
    token = request.cookies.get("jwt")

    if not token:
        return templates.TemplateResponse("profile.html", {"request": request, "response": res})
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
    except jwt.exceptions.ExpiredSignatureError:
        return templates.TemplateResponse("profile.html", {"request": request, "response": res})
    return templates.TemplateResponse("profile.html", {"request": request, "nick": payload["sub"], "response": res})
