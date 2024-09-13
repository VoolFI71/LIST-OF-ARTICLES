from fastapi import APIRouter, HTTPException, Response
from pydantic_models import Reg_User, User as model_user
import sqlite3, jwt, time
from config import secret_key, salt, check_token
import hashlib
from fastapi.templating import Jinja2Templates
from fastapi import Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse, RedirectResponse
from routers.auth import hash_password
from fastapi import UploadFile, File, Depends
from pathlib import Path
import os
setting_profile_router = APIRouter()
templates = Jinja2Templates(directory="front/templates")

@setting_profile_router.get("/settings")
def setting_profile(request: Request, nick: str = Depends(check_token)):
    if nick is None:
        return templates.TemplateResponse("settings_profile.html", {"request": request})
    return templates.TemplateResponse("settings_profile.html", {"request": request, "nick": nick})

def find_files(directory, pattern):
    path = Path(directory)
    return list(path.rglob(pattern))

directory = os.path.abspath("front/avatars")


@setting_profile_router.post("/settings")
def setting_profile(
    username: str = Form(None),
    text1: str = Form(None), 
    text2: str = Form(None), 
    text3: str = Form(None), 
    text4: str = Form(None), 
    file: UploadFile = File(None)
    ):
    if file:
        user_file_path = os.path.join(directory, f"{username}.png")
        if os.path.exists(user_file_path):
            os.remove(user_file_path)
        with open(user_file_path, "wb") as buffer:
            buffer.write(file.file.read())
        return True