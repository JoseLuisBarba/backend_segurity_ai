from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr 
from datetime import datetime
from datetime import date

class CitizenCreate(BaseModel):
    dni: str
    firstname: str 
    lastname: str 
    fathername: str 
    mothername: str 
    birthdate: date
    img: Optional[str] = None

    address: str
    telephone: Optional[str] = None
    cellphone: Optional[str] = None
    email: Optional[EmailStr] = None

class CitizenUpdate(BaseModel):
    firstname: Optional[str] = None 
    lastname: Optional[str] = None 
    fathername: Optional[str] = None 
    mothername: Optional[str] = None 
    birthdate: Optional[date] = None 
    img: Optional[str] = None
    address: Optional[str] = None 
    telephone: Optional[str] = None
    cellphone: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None 


class CitizenOut(BaseModel):
    dni: str
    firstname: str 
    lastname: str 
    fathername: str 
    mothername: str 
    birthdate: date
    img: Optional[str] = None

    address: str
    telephone: Optional[str] = None
    cellphone: Optional[str] = None
    email: Optional[EmailStr] = None
    
    is_active: bool
    createdAt: datetime
    updatedAt:  Optional[datetime] = None
    deletedAt: Optional[datetime] = None


class CitizensOut(BaseModel):
    data: list[CitizenOut]
    count: int