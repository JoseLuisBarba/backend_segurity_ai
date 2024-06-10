from typing import Optional, List
from pydantic import BaseModel, Field 
from datetime import datetime



class RoleCreate(BaseModel):
    name: str = Field(..., description="role name")
    description: str = Field(..., description="role description")

class RoleUpdate(BaseModel):
    name: Optional[str] = Field(..., description="role name")
    description: Optional[str] = Field(..., description="role description")
    is_active: Optional[bool] = Field(..., description="active role")

class RoleId(BaseModel):
    id: int = Field(..., description="role id")

class RoleOut(BaseModel):
    id: int
    name: str 
    description: str 
    is_active: bool
    createdAt: datetime
    updatedAt:  Optional[datetime] = None
    deletedAt: Optional[datetime] = None

class RoleRemove(BaseModel):
    status: bool
    detail: str

class RoleResponse(BaseModel):
    rol: Optional[RoleOut]
    detail: str 

class RolesResponse(BaseModel):
    roles: Optional[List[RoleOut]]
    detail: str 
