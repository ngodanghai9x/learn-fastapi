from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import Optional, Type, TypeVar, cast
from fastapi import HTTPException, status, UploadFile

# DATABASE_URL = "sqlite:///./test.db"
# ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
DATABASE_URL = "postgresql://postgres:postgres@0.0.0.0:5432/fastapidb"
ASYNC_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/fastapidb"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Khởi tạo database
Base.metadata.create_all(bind=engine)

# Hàm dùng chung để tạo session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async_session = sessionmaker(create_async_engine(ASYNC_DATABASE_URL, echo=True), expire_on_commit=False, class_=AsyncSession)

async def get_async_db() -> AsyncSession:
    async with async_session() as session:
        yield session

DBModelT = TypeVar("DBModelT")


async def find_instance_or_fail(
    db: AsyncSession,
    model: Type[DBModelT],
    *args,
    message_404: Optional[str] = None,
) -> DBModelT:
    if message_404 is None:
        message_404 = f"Not found for {model.__name__}"

    instance: Optional[DBModelT] = await db.scalar(select(model).where(*args))

    if instance is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            message_404,
        )

    return cast(DBModelT, instance)

# await db.delete(
#     await find_instance_or_fail(
#         db,
#         User,
#         User.user_id == user_id,
#         message_404=f"Not found for user with user_id {user_id}",
#     )
# )
# await db.commit()
