from fastapi import APIRouter, Form, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic_models import Reg_User, User as model_user
import sqlite3
import jwt
router_delete_user = APIRouter()

templates = Jinja2Templates(directory="front/templates")




@router_delete_user.get("/user/delete/", response_class=HTMLResponse)
def delete_user(request: Request):
    return templates.TemplateResponse("delete.html", {"request": request})

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
            return JSONResponse(content={"detail": "У вас нет доступа"}, status_code=403)

        cursor.execute("DELETE FROM logins WHERE nick=?", (nick,))
        if cursor.rowcount == 0:
            return JSONResponse(content={"detail": "Пользователь не найден"}, status_code=404)
        db.commit()
        
        return JSONResponse(content={"detail": "Пользователь удален"})