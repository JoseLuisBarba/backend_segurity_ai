from typing import Optional
from pydantic import BaseModel, EmailStr, Field 
from datetime import datetime
from datetime import date
from uuid import UUID

class UserCreate(BaseModel):
    id: str
    email: EmailStr
    password: str
    is_superuser: bool
    name: str
    lastname: str
    phone: str
    birthdate: date
    
class UserRegister(BaseModel):
    id: str
    email: EmailStr
    password: str
    name: str
    lastname: str
    phone: str
    birthdate: date

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    name: Optional[str] = None
    lastname: Optional[str]   = None
    is_superuser: Optional[bool] = None
    phone: Optional[str] = None
    birthdate: Optional[date]  = None
    is_active: Optional[bool] = None


class UserUpdateMe(BaseModel):
    name: Optional[str] 
    lastname:Optional[str] 
    new_password: Optional[str] 


class UpdatePassword(BaseModel):
    current_password: str 
    new_password: str


class UserPublic(BaseModel):
    id: str 
    is_superuser: Optional[bool] = None
    email: EmailStr
    name: str
    lastname: str
    phone: str
    birthdate: date
    img: Optional[str] = None
    is_active: Optional[bool] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None


class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int