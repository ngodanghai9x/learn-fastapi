from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

# class CompanyCreate(CompanyBase):
#     pass

class UserResponse(UserBase):
    id: int

    class Config:
        # orm_mode = True # legacy config key
        from_attributes = True
