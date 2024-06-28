from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class IncidenceStatusCreate(BaseModel):
    name: str 
    description: str
    user_id: str    
    is_active: bool
    createdAt: datetime
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None
   
class IncidenceStatusOut(BaseModel):
    id: int
    name: str 
    description: str
    user_id: str    
    is_active: Optional[bool] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None

class ListStatusOut(BaseModel):
    data: list[IncidenceStatusOut]
    count: int

class IncidenceStatusUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None  
    is_active: Optional[bool] = None