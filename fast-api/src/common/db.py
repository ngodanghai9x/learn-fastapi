from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./test.db"

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
