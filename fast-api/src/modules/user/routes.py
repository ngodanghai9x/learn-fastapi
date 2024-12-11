from fastapi import FastAPI
from pprint import pprint
from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status,
    Security,
)
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from modules.user import service, dto
from common.db import get_db, get_async_db

router = APIRouter(
    # include_in_schema=True,
    prefix="/users",
    # tags=["user"],
    # dependencies=[Depends(has_user_token)],
)

@router.post("/", response_model=dto.UserResponse)
async def create_user(user: dto.UserCreate, db: AsyncSession = Depends(get_async_db)):
    db_user = await service.get_user_by_email(db, email=user.email)

    pprint(db_user)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return await service.create_user(db=db, user=user)

@router.get("/{user_id}", response_model=dto.UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    db_user = await service.get_user(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user

@router.get("/", response_model=list[dto.UserResponse])
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_async_db)):
    return await service.get_users(db, skip=skip, limit=limit)

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    db_user = await service.delete_user(db, user_id=user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"detail": "User deleted"}
