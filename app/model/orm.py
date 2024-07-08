import uuid
from typing import List 
from sqlalchemy import (
    Column, ForeignKey, Integer, String, Float, Text,
    Boolean, DateTime, Date, Uuid, Time
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.db import Base


class UserRole(Base):
    __tablename__ = "user_role"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(15), ForeignKey("user.id"), nullable= False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    is_active = Column(Boolean, index=True, default=True, nullable=False)
    createdAt = Column(DateTime, index=True, server_default= func.now(), nullable=False)
    updatedAt = Column(DateTime, nullable=True)
    deletedAt = Column(DateTime, nullable=True)
    
    user = relationship('User')
    role = relationship('Role')


# segurity ai
class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(20), unique=True ,nullable=False)
    description = Column(String(100), nullable=True)

    # auditoria
    is_active = Column(Boolean, index=True, default=True)
    createdAt = Column(DateTime, server_default= func.now(), nullable=False)
    updatedAt = Column(DateTime, nullable=True)
    deletedAt = Column(DateTime, nullable=True)

    class Config:
        orm_mode = True


# segurity ai
class User(Base):
    
    __tablename__ = "user"

    id = Column(String(15), primary_key=True)
    email = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_superuser = Column(Boolean, default=False)

    name = Column(String(25), nullable=False)
    lastname = Column(String(25), nullable=False, index=True)
    phone = Column(String(15), nullable=False, index=True)
    birthdate = Column(Date, nullable=False)
    img = Column(String(255), nullable=True)

    # auditoria
    is_active = Column(Boolean, index=True, default=True)
    createdAt = Column(DateTime, server_default= func.now())
    updatedAt = Column(DateTime, nullable=True)
    deletedAt = Column(DateTime, nullable=True)

class Citizen(Base):

    __tablename__ = "citizen"

    # identification data
    dni = Column(String(15), primary_key=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), index=True, nullable=False)
    fathername = Column(String(100), index=True, nullable=False)
    mothername = Column(String(100), index=True, nullable=False)

    # contact data
    birthdate = Column(Date, nullable=False)
    img = Column(String(255), index=True, nullable=True)
    address = Column(String(120), nullable=False)
    telephone = Column(String(15), nullable=True, index=True)
    cellphone = Column(String(15), nullable=True, index=True)
    email = Column(String(50),  unique=True, index=True, nullable=True)

    # auditoria
    is_active = Column(Boolean, index=True, default=True)
    createdAt = Column(DateTime, server_default= func.now())
    updatedAt = Column(DateTime, nullable=True)
    deletedAt = Column(DateTime, nullable=True)


class IncidenceType(Base):

    __tablename__ = "incidence_type"

    id = Column( Integer, primary_key=True, autoincrement="auto")
    name = Column(String(20), unique=True, index=True, nullable=False)
    description = Column(String(100), nullable=True)
    user_id = Column(String(15), ForeignKey("user.id"), nullable= False)
    # auditoria
    is_active = Column(Boolean, index=True, default=True)
    createdAt = Column(DateTime, server_default= func.now())
    updatedAt = Column(DateTime, nullable=True)
    deletedAt = Column(DateTime, nullable=True)

    user = relationship('User')

class IncidenceStatus(Base):

    __tablename__ = "incidence_status"

    id = Column( Integer, primary_key=True, autoincrement="auto")
    name = Column(String(20), unique=True, index=True, nullable=False)
    description = Column(String(100), nullable=True)
    user_id = Column(String(15), ForeignKey("user.id"), nullable= False)
    # auditoria
    is_active = Column(Boolean, index=True, default=True)
    createdAt = Column(DateTime, server_default= func.now())
    updatedAt = Column(DateTime, nullable=True)
    deletedAt = Column(DateTime, nullable=True)

    user = relationship('User')
                      

class IncidentPerpetrator(Base):
    __tablename__ = "incident_perpetrator"

    id = Column(Integer, primary_key=True, autoincrement=True)
    perpetrator_id = Column(Integer, ForeignKey("perpetrator.id"), nullable=False)
    incident_id = Column(Integer, ForeignKey("incidence.id"), nullable=False)

    # auditoria
    is_active = Column(Boolean, index=True, default=True, nullable=False)
    createdAt = Column(DateTime, index=True, server_default= func.now(), nullable=False)
    updatedAt = Column(DateTime, nullable=True)
    deletedAt = Column(DateTime, nullable=True)
    
    perpetrator = relationship('Perpetrator')
    incidence = relationship('Incidence')


class Perpetrator(Base):
    __tablename__ = "perpetrator"
    id = Column(Integer, primary_key=True, autoincrement=True)
    dni = Column(String(15), unique=True, nullable=True)
    firstname = Column(String(50), nullable=True)
    lastname = Column(String(50), index=True, nullable=True)
    person_details = Column(Text, nullable=False)
    age = Column(Integer, nullable=False)
    img = Column(String(255), nullable=True)
    # auditoria
    is_active = Column(Boolean, index=True, default=True, nullable=False)
    createdAt = Column(DateTime, index=True, server_default= func.now(), nullable=False)
    updatedAt = Column(DateTime, nullable=True)
    deletedAt = Column(DateTime, nullable=True)


class Incidence(Base):

    __tablename__ = "incidence"

    id = Column( Integer, primary_key=True, autoincrement="auto")
    description = Column(Text, nullable=False)

    type_id = Column(Integer, ForeignKey("incidence_type.id"), nullable= False)
    status_id = Column(Integer, ForeignKey("incidence_status.id"), nullable= False)
    user_id = Column(String(15), ForeignKey("user.id"), nullable= False)
    citizen_id = Column(String(15), ForeignKey("citizen.dni"), nullable= False)

    # Incident Description
    # Location
    longitude = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True) 
    address = Column(String(120), nullable=False)
    # Date and time
    date_incident = Column(Date, nullable=False)
    time_incident = Column(Time, nullable=False)
    # Incident Details
    inciden_details = Column(Text, nullable=False)

    # auditoria
    is_active = Column(Boolean, index=True, default=True)
    createdAt = Column(DateTime, server_default= func.now())
    updatedAt = Column(DateTime, nullable=True)
    deletedAt = Column(DateTime, nullable=True)

    type = relationship("IncidenceType")
    status = relationship("IncidenceStatus")
    user = relationship("User")
    citizen = relationship("Citizen")




    




