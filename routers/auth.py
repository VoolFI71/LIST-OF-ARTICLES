from fastapi import APIRouter, HTTPException, Response
from pydantic_models import Reg_User, User as model_user
import sqlite3
import jwt
router_auth = APIRouter()
import time
from config import secret_key

@router_auth.post("/user/register")
def create_user(user: Reg_User):
    if user.password!=user.password2:
        return {"message": "passwords are incorrect"}
    try:
        with sqlite3.connect("db/database.db") as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO logins (nick, password) VALUES (?, ?)", (user.nick, user.password))
            db.commit()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "User created successfully"}

@router_auth.get("/user/login")
def login_user(user: model_user, response: Response):
    with sqlite3.connect("db/database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM logins WHERE nick=?", (user.nick,))
        rows = cursor.fetchall()

        if rows and rows[0][1]==user.password:
            token = jwt.encode({"sub": user.nick, "hash_password": user.password, "exp": int(time.time())+30}, secret_key, algorithm='HS256')
            response.set_cookie(key="jwt", value=token, httponly=True, secure=False)
            cursor.execute("UPDATE logins SET token=? WHERE nick=?", (token, user.nick))
            db.commit()
            return {"message": "You are logged in", "token": token}
        return {"message": "You are no logged"}