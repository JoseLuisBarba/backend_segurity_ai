from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr 
from datetime import datetime
from datetime import date, time


class IncidenceCreate(BaseModel):
    description: str 
    type_id: int 
    status_id: int
    user_id: str
    citizen_id: str 
    longitude: Optional[float] = None 
    latitude: Optional[float] = None 
    address: str 
    date_incident: date 
    time_incident: time
    inciden_details: str 
    is_active: bool
    createdAt: datetime
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None


class IncidenceTypeOut(BaseModel):
    id: int
    name: str

class IncidenceStatusOut(BaseModel):
    id: int
    name: str

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
    email: Optional[str] = None

class IncidenceOut(BaseModel):
    id: int
    description: str
    type: IncidenceTypeOut
    status: IncidenceStatusOut
    citizen: CitizenOut
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    address: str
    date_incident: date
    time_incident: time
    inciden_details: str
    is_active: bool
    createdAt: datetime
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None

class IncidencesOut(BaseModel):
    data: List[IncidenceOut]
    count: int


class IncidenceCreateOut(BaseModel):
    id: int
    description: str 
    type_id: int 
    status_id: int
    user_id: str
    citizen_id: str 
    longitude: Optional[float] = None 
    latitude: Optional[float] = None 
    address: str 
    date_incident: date 
    time_incident: time
    inciden_details: str 
    is_active: Optional[bool] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None


