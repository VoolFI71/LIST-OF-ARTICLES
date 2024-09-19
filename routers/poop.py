import json
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi import Path
from pydantic import BaseModel
from fastapi.responses import FileResponse
import uvicorn
from fastapi import FastAPI, Cookie, Request, Response, Depends, WebSocketDisconnect
from fastapi import Body, Header, WebSocket
from fastapi import HTTPException
from routers.auth import router_auth
from routers.delete_user import router_delete_user
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers.login import router_login
from routers.register import router_reg
from routers.profile import router_profile
from routers.users import router_users
from routers.lists import router_lists
from config import secret_key, check_token, check_token_ws, ConnectionManager, ChatManager
from routers.main_page import main_page_router as router_main_page
from routers.setting_profile import setting_profile_router
import os, redis, aiosqlite
from pydantic_models import Message
import time
from db import models
from fastapi import APIRouter
pop = APIRouter()

@pop.post("/chat")
async def messages(message: Message):
    try:
       async with aiosqlite.connect("db/database.db") as db:
            await manager_chat.broadcast(message)
            it = time.time()
            await db.execute("INSERT INTO chat (message, id) VALUES (?, ?)", (message.message, it, ))
            await db.commit()
            return {"status": "success", "message": "Message added successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to add message")



@pop.get("/profile/avatars/{nick}")
def main(nick: str = Path(...)):
    image_path = os.path.abspath(f"front/avatars/{nick}.png")
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        return {"error": "Image not found"}, 404