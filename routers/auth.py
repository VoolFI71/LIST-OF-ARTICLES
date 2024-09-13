from fastapi import APIRouter, HTTPException, Response
import sqlite3
from config import secret_key, salt
import hashlib
from fastapi import Request, Form

router_auth = APIRouter()

def hash_password(password: str) -> str:
    sha256 = hashlib.sha256()

    sha256.update((password+salt).encode('utf-8'))

    hashed_password = sha256.hexdigest()

    return hashed_password
