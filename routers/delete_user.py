from fastapi import APIRouter, Form, HTTPException, Request, Response, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import sqlite3
import jwt
from config import secret_key, check_token
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

    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT role FROM logins WHERE token=?", (token,))
        result = cursor.fetchone()

        if result is None or result[0] != "admin":
            return JSONResponse(content={"detail": "У вас нет доступа"})

        cursor.execute("DELETE FROM logins WHERE nick=?", (nick,))
        if cursor.rowcount == 0:
            return JSONResponse(content={"detail": "Пользователь не найден"})
        db.commit()

        return JSONResponse(content={"detail": "Пользователь удален"})