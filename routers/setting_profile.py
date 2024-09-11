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

setting_profile_router = APIRouter()
templates = Jinja2Templates(directory="front/templates")

@setting_profile_router.get("/settings")
def setting_profile(request: Request):
    token = request.cookies.get("jwt")
    if not token:
        return templates.TemplateResponse("settings_profile.html", {"request": request})
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
    except:
        return templates.TemplateResponse("settings_profile.html", {"request": request})
    return templates.TemplateResponse("settings_profile.html", {"request": request, "nick": payload["sub"]})

@setting_profile_router.post("/settings")
def setting_profile(request: Request):
    return templates.TemplateResponse("settings_profile.html", {"request": request})
#