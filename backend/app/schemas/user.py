from pydantic import BaseModel, EmailStr,Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str=Field(..., max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str=Field(..., min_length=6,max_length=72)
    avatar: Optional[str] = "default.jpg"

class UserUpdate(BaseModel):
    username: Optional[str]=Field(None, max_length=50)
    email: Optional[EmailStr] = None

class ChangePassword(BaseModel):
    old_password: Optional[str]=Field(..., max_length=50)
    new_password: Optional[str]=Field(..., min_length=6,max_length=72)

class UserResponse(UserBase):
    id: int
    created_at: datetime
    email: EmailStr
    is_active:bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None