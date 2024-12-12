from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String
# from common.db import Base
from src.common.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    json_data = Column(JSONB, default=dict)  # Cột jsonb
    phone_no = Column(String, nullable=True, unique=True, default=None)