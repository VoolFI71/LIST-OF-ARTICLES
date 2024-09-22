from fastapi import APIRouter, HTTPException, Response
from pydantic_models import Reg_User, User as model_user
import sqlite3
import jwt
import time
from config import secret_key, salt
import hashlib
from fastapi.templating import Jinja2Templates
from fastapi import Request, Form, Depends, Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse, RedirectResponse
from routers.auth import hash_password
from config import check_token
from db.database2 import engine
from db.database2 import ss
from sqlalchemy import text
router_profile= APIRouter()
templates = Jinja2Templates(directory="front/templates")

@router_profile.get("/profile/{nick}")
def get_profile(request: Request, name: str = Depends(check_token), nick: str = Path(...)):
    with ss() as session:
        res = session.execute(text("SELECT * FROM logins WHERE nick=:nick"), {"nick": nick}).fetchone()

    if res is None:
        raise HTTPException(status_code=404, detail="User not found")
    if nick is None:
        return templates.TemplateResponse("profile.html", {"request": request, "response": res})
    return templates.TemplateResponse("profile.html", {"request": request, "nick": name, "response": res})
 