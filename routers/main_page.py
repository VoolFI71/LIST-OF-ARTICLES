from fastapi import Request, Depends, APIRouter
from fastapi.templating import Jinja2Templates
import jwt
from config import secret_key, check_token

main_page_router  = APIRouter()

templates = Jinja2Templates(directory="front/templates")

@main_page_router.get("/")
def main(request: Request, nick: str = Depends(check_token)):
    if nick is None:
        return templates.TemplateResponse("main.html", {"request": request})
    return templates.TemplateResponse("main.html", {"request": request, "nick": nick})

