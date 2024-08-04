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
