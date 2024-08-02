from fastapi import APIRouter, HTTPException, Response
from pydantic_models import Reg_User, User as model_user
import sqlite3
import jwt
router_delete_user = APIRouter()

@router_delete_user.delete("/user/delete/{nick}")
def delete_user(nick: str):
    try:
        with sqlite3.connect("db/database.db") as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM logins WHERE nick=?", (nick,))
            db.commit()
            if cursor.rowcount == 0:  # Проверка, был ли удален хоть один элемент
                raise HTTPException(status_code=404, detail="User with {nick} not found")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Expense deleted successfully"}