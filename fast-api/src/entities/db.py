from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from src.configs.env_setting import env


# DATABASE_URL = "sqlite:///./test.db"
# ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
DATABASE_URL       = f"postgresql://{env.DB_USER}:{env.DB_PASSWORD.get_secret_value()}@{env.DB_HOST}:{env.DB_PORT}/{env.DB_NAME}"
ASYNC_DATABASE_URL = f"postgresql+asyncpg://{env.DB_USER}:{env.DB_PASSWORD.get_secret_value()}@{env.DB_HOST}:{env.DB_PORT}/{env.DB_NAME}"
print("🐍 File: entities/db.py | Line: 12 | undefined ~ ASYNC_DATABASE_URL",ASYNC_DATABASE_URL)

Base = declarative_base()
engine = create_engine(DATABASE_URL)
# Khởi tạo database
Base.metadata.create_all(bind=engine)

SessionDb = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db() -> Session:
    db = SessionDb()
    try:
        yield db
    finally:
        db.close()


AsyncSessionDb = sessionmaker(create_async_engine(ASYNC_DATABASE_URL, echo=True), expire_on_commit=False, class_=AsyncSession)
async def get_async_db() -> AsyncSession:
    async with AsyncSessionDb() as session:
        yield session


