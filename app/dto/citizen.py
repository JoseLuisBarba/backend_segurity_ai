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


class CitizenInfo(BaseModel):
    nombre: Optional[str]
    tipoDocumento: Optional[str]
    numeroDocumento: Optional[str]
    estado: Optional[str]
    condicion: Optional[str]
    direccion: Optional[str]
    ubigeo: Optional[str]
    viaTipo: Optional[str]
    viaNombre: Optional[str]
    zonaCodigo: Optional[str]
    zonaTipo: Optional[str]
    numero: Optional[str]
    interior: Optional[str]
    lote: Optional[str]
    dpto: Optional[str]
    manzana: Optional[str]
    kilometro: Optional[str]
    distrito: Optional[str]
    provincia: Optional[str]
    departamento: Optional[str]
    nombres: Optional[str]
    apellidoPaterno: Optional[str]
    apellidoMaterno: Optional[str]