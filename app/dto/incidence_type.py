from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr 
from datetime import datetime
from datetime import date

class IncidenceTypeCreate(BaseModel):
    name: str 
    description: str
    user_id: str    
    is_active: bool
    createdAt: datetime
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None
   
class IncidenceTypeOut(BaseModel):
    id: int
    name: str 
    description: str
    user_id: str    
    is_active: Optional[bool] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None

class IncidenceTypesOut(BaseModel):
    data: list[IncidenceTypeOut]
    count: int

class IncidenceTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None  
    is_active: Optional[bool] = None





