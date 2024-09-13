from fastapi import Request
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
import jwt
from config import secret_key
main_page_router  = APIRouter()

templates = Jinja2Templates(directory="front/templates")

@main_page_router.get("/")
def main(request: Request):
    token = request.cookies.get("jwt")
    if not token:
        return templates.TemplateResponse("main.html", {"request": request})
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
    except:
        return templates.TemplateResponse("main.html", {"request": request})

    return templates.TemplateResponse("main.html", {"request": request, "nick": payload["sub"]})

