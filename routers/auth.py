from fastapi import APIRouter, HTTPException, Response
import sqlite3
from config import secret_key, salt
import hashlib
from fastapi import Request, Form

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
