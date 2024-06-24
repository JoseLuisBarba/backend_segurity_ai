from app.model.orm import IncidenceType
from app.dto.incidence_type import (
    IncidenceTypeOut, IncidenceTypesOut, IncidenceTypeCreate,
    IncidenceTypeUpdate
)
from app.helpers.convertions import make_naive
from app.helpers.incidence_type import (
    to_incidence_type_out
)



from sqlalchemy.sql import select, update, func
from typing import Optional
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone

async def get_incidences_type(
        *, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> Optional[IncidenceTypesOut]:
    count_query = (
        select(func.count())
        .select_from(IncidenceType)
        .where(IncidenceType.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    response = await session.scalar(count_query)
    type_count = int(response)
    type_query = (
        select(IncidenceType).where(IncidenceType.is_active == True).offset(skip).limit(limit)
    )
    types: list[IncidenceType] = await session.scalars(type_query)

    roles_out: list[IncidenceTypeOut] = [ 
        to_incidence_type_out(type_in=type_data) for type_data in types 
    ]

    return IncidenceTypesOut(data=roles_out, count=type_count)

async def get_incidence_type_by_name(
        *, session: AsyncSession, incidence_type_name= str
    ) -> Optional[IncidenceTypeOut]:
    try:
        query = (
            select(IncidenceType).where(IncidenceType.name == incidence_type_name).limit(1)
        )
        type = await session.scalar(query)
        if not type:
            return None
        return type
    except SQLAlchemyError as err:
        return None 
    

async def get_role_by_id(
        *, session: AsyncSession, type_id= int
    ) -> Optional[IncidenceTypeOut]:
    try:
        query = (
            select(IncidenceType).where(IncidenceType.id == type_id).limit(1)
        )
        type: IncidenceType = await session.scalar(query)
        if not type:
            return None
        return to_incidence_type_out(type_in=type)
    
    except SQLAlchemyError as err:
        return None 
    
async def create_incidence_type(
        *, session: AsyncSession, incidence_type_create= IncidenceTypeCreate
    ) -> Optional[IncidenceTypeOut]:
    try:
        type_out: IncidenceTypeOut = await get_incidence_type_by_name(
            session=session, incidence_type_name=incidence_type_create.name
        )
        if type_out:
            return None
        type_in = IncidenceType(
            name= incidence_type_create.name,
            description= incidence_type_create.description,
            user_id= incidence_type_create.user_id,
            is_active= True,
            createdAt= make_naive(datetime.now(timezone.utc))
        )
        session.add(type_in)
        await session.commit()
        await session.refresh(type_in)
        if not type_in:
            return None
        return to_incidence_type_out(type_in=type_in)
    except SQLAlchemyError as err:
        await session.rollback()
        return None
    
async def update_incidence_type(
        *, session: AsyncSession, current_type: IncidenceType, type_in: IncidenceTypeUpdate
    ) -> Optional[IncidenceTypeOut]:
    try:
        update_data = type_in.model_dump(exclude_unset=True)
        extra_data = {}
        extra_data["updatedAt"] = make_naive(datetime.now(timezone.utc))
    
        if "is_active" in update_data:
            if not bool(update_data["is_active"]):
                update_data["is_active"] = False
                extra_data["deletedAt"] = make_naive(datetime.now(timezone.utc))
            else:
                extra_data["deletedAt"] = None
       
        #current_type <- actualiza los campos con update_data y extra_data
        for field, value in update_data.items():
            if value is not None:
                setattr(current_type, field, value)
        
        for field, value in extra_data.items():
            setattr(current_type, field, value)

        session.add(current_type)
        await session.commit()
        await session.refresh(current_type)
        return to_incidence_type_out(type_in=current_type)
    except SQLAlchemyError as err:
        await session.rollback()
        return None