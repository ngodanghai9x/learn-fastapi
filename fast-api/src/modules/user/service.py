from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from src.entities import User
from src.modules.user import dto
from src.modules.user import repo
from pprint import pprint

# Create user
async def create_user(db: AsyncSession, user: dto.UserCreate) -> User:
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=user.password,
        json_data={"dict": True, "num": 123},  # Lưu dữ liệu json
        # json_data=user.json_data,  # Lưu dữ liệu json
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)  # Tải lại đối tượng sau khi commit
    return db_user

# Get user by ID
async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()  # Lấy kết quả đầu tiên hoặc None

# Get user by email
async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

# Get all users
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

# Update user
async def update_user(db: AsyncSession, user_id: int, user: dto.UserUpdate) -> User:
    db_user = await repo.get_user(db, user_id)
    if not db_user:
        raise NoResultFound("User not found")


    for key, value in user.model_dump(exclude_unset=True).items():
    # for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user


# Delete user
async def delete_user(db: AsyncSession, user_id: int):
    db_user = await repo.get_user(db, user_id)
    print("🐍 File: user/ser db_user",db_user.__dict__)

    # print(db_user)
    if not db_user:
        raise NoResultFound("User not found")
    await db.delete(db_user)
    await db.commit()

    return db_user.__dict__
