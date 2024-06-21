from typing import Any, Optional
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
from app.model.orm import User, Role
from app.dto.user import UserCreate, UserUpdate
from app.dto.role import RoleCreate, RoleOut, RolesOut

from datetime import datetime, timezone
from datetime import date
from sqlalchemy.sql import select, update, func


def make_naive(dt):
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt

def to_role_out(role_in: Role)->RoleOut:
    return RoleOut(
        id= role_in.id, 
        name= role_in.name, 
        description= role_in.description, 
        is_active= role_in.is_active, 
        createdAt= role_in.createdAt, 
        updatedAt= role_in.updatedAt,
        deletedAt= role_in.deletedAt
    )


async def get_roles(
        *, session: AsyncSession, skip: int = 0, limit: int = 100
    ):
    count_query = (
        select(func.count()).select_from(Role).where(Role.is_active == True).offset(skip).limit(limit)
    )
    response = await session.scalar(count_query)

    role_count = int(response)
    roles_query = (
        select(Role).where(Role.is_active == True).offset(skip).limit(limit)
    )
    roles: list[Role] = await session.scalars(roles_query)

    roles_out: list[RoleOut] = [ 
        to_role_out(role_in=role_data) for role_data in roles 
    ]

    return RolesOut(data=roles_out, count=role_count)



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
        return None 
    

async def get_role_by_id(
        *, session: AsyncSession, role_id= int
    ) -> Optional[RoleOut]:
    try:
        query = (
            select(Role).where(Role.id == role_id).limit(1)
        )
        role: Role = await session.scalar(query)
        if not role:
            return None
        return to_role_out(role_in=role)
    
    except SQLAlchemyError as err:
        return None 

async def create_role(
        *, session: AsyncSession, role_create= RoleCreate
    ) -> Optional[RoleOut]:
    try:
        role_out = await get_role_by_name(
            session=session, 
            role_name=role_create.name
        )
        if role_out:
            return None
        role_in = Role(
            name = role_create.name,
            description = role_create.description,
            is_active = True,
            createdAt = make_naive(datetime.now(timezone.utc))
        )
        session.add(role_in)
        await session.commit()
        await session.refresh(role_in)
        if not role_in:
            return None
        return to_role_out(role_in=role_in)
    except SQLAlchemyError as err:
        await session.rollback()
        return None
    


