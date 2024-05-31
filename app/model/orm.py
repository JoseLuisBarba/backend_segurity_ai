import uuid
from typing import List 
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Date, Uuid
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
    rol = relationship('Role')


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





# class UserRole(Base):
#     __tablename__ = "user_role"

#     id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     user_id = Column(String(15), ForeignKey("user.dni"), nullable= False)
#     role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
#     is_active = Column(Boolean, index=True, default=True, nullable=False)
#     createdAt = Column(DateTime, index=True, server_default= func.now(), nullable=False)
#     updatedAt = Column(DateTime, nullable=True)
#     deletedAt = Column(DateTime, nullable=True)
    
#     user = relationship('User')
#     rol = relationship('Role')


# # segurity ai
# class Role(Base):
#     __tablename__ = "role"
#     id = Column(Integer, primary_key=True, autoincrement="auto")
#     name = Column(String(20), unique=True ,nullable=False)
#     description = Column(String(100), nullable=True)

#     # auditoria
#     is_active = Column(Boolean, index=True, default=True)
#     createdAt = Column(DateTime, server_default= func.now(), nullable=False)
#     updatedAt = Column(DateTime, nullable=True)
#     deletedAt = Column(DateTime, nullable=True)




# # segurity ai
# class User(Base):
    
#     __tablename__ = "user"

#     dni = Column(String(15), primary_key=True)
#     email = Column(String(50), unique=True, nullable=False)
#     password = Column(String(25), nullable=False)
#     name = Column(String(25), nullable=False)
#     lastname = Column(String(25), nullable=False, index=True)
#     phone = Column(String(15), nullable=False, index=True)
#     birthdate = Column(Date, nullable=False)
#     img = Column(String(255), nullable=True)

#     # auditoria
#     is_active = Column(Boolean, index=True, default=True)
#     createdAt = Column(DateTime, server_default= func.now())
#     updatedAt = Column(DateTime, nullable=True)
#     deletedAt = Column(DateTime, nullable=True)