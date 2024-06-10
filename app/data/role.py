from typing import Any, Optional
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
from app.model.orm import User, Role
from app.dto.user import UserCreate, UserUpdate
from app.dto.role import RoleCreate

from datetime import datetime, timezone
from datetime import date


def make_naive(dt):
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt

async def get_role_by_name(
        *, session: AsyncSession, role_name= str
    ) -> Optional[Role]:
    try:
        query = (
            select(Role).where(Role.name == role_name).limit(1)
        )
        role = await session.scalar(query)
        if not role:
            return None
        return role
    except SQLAlchemyError as err:
        raise None 
    

async def get_role_by_id(
        *, session: AsyncSession, role_id= int
    ) -> Optional[Role]:
    try:
        query = (
            select(Role).where(Role.id == role_id).limit(1)
        )
        role = await session.scalar(query)
        if not role:
            return None
        return role
    except SQLAlchemyError as err:
        raise None    

async def createRole(
        *, session: AsyncSession, role_create= RoleCreate
    ):
    try:

        role_out = get_role_by_name(
            session=session, 
            role_name=role_create.name
        )
        if role_out:
            return None

        rol_in = Role(
            name = role_create.name,
            description = role_create.description,
            is_active = True,
            createdAt = make_naive(datetime.now(timezone.utc))
        )
        session.add(rol_in)
        await session.commit()
        await session.refresh(rol_in)
        if not rol_in:
            return None
        return rol_in
    except SQLAlchemyError as err:
        await session.rollback()
        raise None
    
