from pydantic import BaseModel, EmailStr
from typing import Optional, Dict

class UserBase(BaseModel):
    name: str
    email: EmailStr
    # json_data: Optional[Dict] = {}  # Hỗ trợ dữ liệu JSON

class UserCreate(UserBase):
    password: str

# class CompanyCreate(CompanyBase):
#     pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    # json_data: Optional[Dict] = None

class UserResponse(UserBase):
    id: int

    class Config:
        # orm_mode = True # legacy config key
        from_attributes = True
