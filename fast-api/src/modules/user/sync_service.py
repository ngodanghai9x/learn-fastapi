from sqlalchemy.orm import Session
from src.entities import User
from src.modules.user import dto

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: dto.UserCreate):
    hashed_password = user.password + "notreallyhashed" 

    db_user = User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)

    db.commit()
    db.refresh(db_user)

    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user:
        db.delete(db_user)
        db.commit()

    return db_user
