from fastapi.templating import Jinja2Templates
import uvicorn
from fastapi import FastAPI, Cookie, Request, Response, Depends
from aiogram import *
from aiogram.types import *
from random import *
from fastapi import Body, Header
from fastapi import FastAPI, Body, HTTPException
from random import *
from pydantic_models import List as model_list
from uuid import uuid4
import jwt
from routers.auth import router_auth
from routers.delete_user import router_delete_user
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers.login import router_login
from routers.register import router_reg
from routers.profile import router_profile
from routers.users import router_users
from routers.lists import router_lists
app = FastAPI()
templates = Jinja2Templates(directory="front/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="front/static"), name="static")
@app.get("/")
def main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


app.include_router(router_auth)
app.include_router(router_delete_user)
app.include_router(router_login)
app.include_router(router_reg)
app.include_router(router_profile)
app.include_router(router_users)
app.include_router(router_lists)