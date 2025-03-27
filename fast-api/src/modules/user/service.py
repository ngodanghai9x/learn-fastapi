from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from src.modules.user import dto as userDto
from src.modules.user import repo as userRepo
from src.modules.user.repo import UserRepo
from pprint import pprint
from src.entities import get_db, get_async_db, User
from fastapi import (
    Depends,
)


# from repositories.user_repo import UserRepo
# from db import get_db
# from sqlalchemy.ext.asyncio import AsyncSession

class UserService:
    def __init__(self):
        self.userRepo = UserRepo()  # Repo sẽ luôn dùng instance duy nhất

    # Create user
    async def create_user(self, body: userDto.UserCreate) -> User:
        res = await self.userRepo.create_user(body) 
        return res

    # Get user by ID
    async def get_user(self, user_id: int) -> User | None:
        res = await self.userRepo.get_user(user_id) 
        return res

    # Get user by email
    async def get_user_by_email(self, email: str) -> User | None:
        res = await self.userRepo.get_user_by_email(email) 
        return res

    # Get all users
    async def get_users(self, skip: int = 0, limit: int = 10) -> list[User]:
        res = await self.userRepo.get_users(skip, limit) 
        return res

    # Update user
    async def update_user(self, user_id: int, body: userDto.UserUpdate) -> User:
        res = await self.userRepo.update_user(user_id, body) 
        return res


    # Delete user
    async def delete_user(self, user_id: int):
        db_user = await self.userRepo.get_user(user_id)
        print("🐍 File: user/ser db_user",db_user.__dict__)

        # if not db_user:
        #     raise NoResultFound("User not found")
        #     # raise HTTPException(status_code=404, detail="User not found")

        res = await self.userRepo.delete_user(db_user) 
        return res

        # return db_user.__dict__

# =================================

# Create user
async def create_user(body: userDto.UserCreate) -> User:
    res = await userRepo.create_user(db, body) 
    return res

# Get user by ID
async def get_user(user_id: int) -> User | None:
    res = await userRepo.get_user(db, user_id) 
    return res

# Get user by email
async def get_user_by_email(email: str) -> User | None:
    res = await userRepo.get_user_by_email(db, email) 
    return res

# Get all users
async def get_users(skip: int = 0, limit: int = 10) -> list[User]:
    res = await userRepo.get_users(db, skip, limit) 
    return res

# Update user
async def update_user(user_id: int, body: userDto.UserUpdate) -> User:
    res = await userRepo.update_user(db, user_id, body) 
    return res


# Delete user
async def delete_user(user_id: int):
    db_user = await userRepo.get_user(db, user_id)
    print("🐍 File: user/ser db_user",db_user.__dict__)

    # if not db_user:
    #     raise NoResultFound("User not found")
    #     # raise HTTPException(status_code=404, detail="User not found")

    res = await userRepo.delete_user(db, db_user) 
    return res

    # return db_user.__dict__
