from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from modules.user import service, dto
from common.db import get_db

router = APIRouter(
    # include_in_schema=True,
    prefix="/template/users",
    # dependencies=[Depends(has_user_token)],
)

# Cấu hình template
templates = Jinja2Templates(directory="src/templates")
# templates = Jinja2Templates(directory="templates")

# Gắn route tĩnh (nếu cần dùng CSS/JS)
# router.mount("/static", StaticFiles(directory="app/static"), name="static")

@router.get("", response_class=HTMLResponse)
def read_users(request: Request, db: Session = Depends(get_db)):
    users = service.get_users(db)

    return templates.TemplateResponse("users/index.html", {"request": request, "users": users})

# must before @router.get("/{user_id}"
@router.get("/new", response_class=HTMLResponse)
def create_user_form(request: Request):
    return templates.TemplateResponse("users/create.html", {"request": request})

@router.get("/{user_id}", response_class=HTMLResponse)
def read_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = service.get_user(db, user_id=user_id)
    if not user:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

    return templates.TemplateResponse("users/detail.html", {"request": request, "user": user})



# @router.post("/", response_class=HTMLResponse)
# def create_user(
#     name: str = Form(...), 
#     email: str = Form(...), 
#     password: str = Form(...), 
#     db: Session = Depends(get_db)
# ):
#     user_data = schemas.UserCreate(name=name, email=email, password=password)
#     service.create_user(db, user=user_data)

#     return HTMLResponse(content="<h1>User Created</h1><a href=''>Back to list</a>")
