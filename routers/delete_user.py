from fastapi import APIRouter, Form, HTTPException, Request, Response, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import sqlite3
import jwt
from config import secret_key, check_token
from db.database2 import engine
from db.database2 import ss
from sqlalchemy import text
router_delete_user = APIRouter()

templates = Jinja2Templates(directory="front/templates")

@router_delete_user.get("/user/delete/", response_class=HTMLResponse)
def delete_user(request: Request, nick: str = Depends(check_token)):
    if nick is None:
        return templates.TemplateResponse("delete.html", {"request": request})
    return templates.TemplateResponse("delete.html", {"request": request, "nick": nick})

@router_delete_user.post("/user/delete/")
def delete_user(request: Request, nick: str = Form(...)):
    token = request.cookies.get("jwt")
    if not token:
        return JSONResponse(content={"detail": "Токен не предоставлен"}, status_code=401)
    nick_user = jwt.decode(token, secret_key, algorithms=['HS256'])["sub"]
    with ss() as session:
        
        result = session.execute(text("SELECT role FROM logins WHERE nick=:nick"), {"nick": nick_user}).fetchone()
        if result is None or result[0] != "admin":
            return JSONResponse(content={"detail": "У вас нет доступа"})

        delete_result = session.execute(text("DELETE FROM logins WHERE nick=:nick"), {"nick": nick})
        
        if delete_result.rowcount == 0:
            return JSONResponse(content={"detail": "Пользователь не найден"}, status_code=404)
        session.commit()

        return JSONResponse(content={"detail": "Пользователь удален"})