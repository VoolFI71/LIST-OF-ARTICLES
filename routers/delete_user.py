from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic_models import Reg_User, User as model_user
import sqlite3
import jwt
router_delete_user = APIRouter()

templates = Jinja2Templates(directory="front/templates")




@router_delete_user.get("/user/delete/", response_class=HTMLResponse)
def delete_user(request: Request):
    return templates.TemplateResponse("delete.html", {"request": request})

@router_delete_user.delete("/user/delete/")
def delete_user(request: Request):
    return {"message": "User deleted"}