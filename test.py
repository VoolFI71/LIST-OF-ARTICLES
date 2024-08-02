from fastapi import APIRouter, HTTPException, Response
from pydantic_models import Reg_User, User as model_user
import sqlite3
import jwt
import time
from config import secret_key
import hashlib
router_auth = APIRouter()

def hash_password(password: str) -> str:
    sha256 = hashlib.sha256()

    sha256.update((password+"salt").encode('utf-8'))

    hashed_password = sha256.hexdigest()

    return hashed_password
print(hash_password("1d"))