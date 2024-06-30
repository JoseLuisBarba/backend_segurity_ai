from app.model.orm import IncidenceStatus
from app.dto.incidence_status import (
    IncidenceStatusOut, IncidenceStatusCreate, IncidenceStatusUpdate, ListStatusOut
)
from app.dto.utils import Message
from app.helpers.convertions import make_naive
from app.helpers.incidence_status import (
    to_incidence_status_out
)


from sqlalchemy.sql import select, update, func
from typing import Optional
from sqlalchemy.sql import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone


async def get_incidence_status_by_name(
        *, session: AsyncSession, name= str
    ) -> Optional[IncidenceStatusOut]:
    try:
        query = (
            select(IncidenceStatus).where(IncidenceStatus.name == name).limit(1)
        )
        status: IncidenceStatus = await session.scalar(query)
        if not type:
            return None
        return status
    except SQLAlchemyError as err:
        return None 
    
async def get_incidences_status(
        *, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> Optional[ListStatusOut]:
    count_query = (
        select(func.count())
        .select_from(IncidenceStatus)
        .where(IncidenceStatus.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    response = await session.scalar(count_query)
    count = int(response)
    status_query = (
        select(IncidenceStatus).where(IncidenceStatus.is_active == True).offset(skip).limit(limit)
    )
    status: list[IncidenceStatus] = await session.scalars(status_query)

    status_out: list[IncidenceStatusOut] = [ 
        to_incidence_status_out(status_in=status_data) for status_data in status
    ]

    return ListStatusOut(data=status_out, count=count)

async def get_incidence_status__by_id(
        *, session: AsyncSession, id= int
    ) -> Optional[IncidenceStatusOut]:
    try:
        query = (
            select(IncidenceStatus).where(IncidenceStatus.id == id).limit(1)
        )
        status: IncidenceStatus = await session.scalar(query)
        if not status:
            return None
        return to_incidence_status_out(status_in=status)
    except SQLAlchemyError as err:
        return None 
    
async def create_incidence_status(
        *, session: AsyncSession, status_create= IncidenceStatusCreate
    ) -> Optional[IncidenceStatusOut]:
    try:
        status_out: IncidenceStatusOut = await get_incidence_status_by_name(
            session=session, name=status_create.name
        )
        if status_out:
            return None
        status_in = IncidenceStatus(
            name= status_create.name,
            description= status_create.description,
            user_id= status_create.user_id,
            is_active= True,
            createdAt= make_naive(datetime.now(timezone.utc))
        )
        session.add(status_in)
        await session.commit()
        await session.refresh(status_in)

        if not status_in:
            return None
        return to_incidence_status_out(status_in=status_in)
    except SQLAlchemyError as err:
        await session.rollback()
        return None
    
async def update_incidence_status(
        *, session: AsyncSession, current_status: IncidenceStatus, status_in: IncidenceStatusUpdate
    ) -> Optional[IncidenceStatusOut]:
    try:
        update_data = status_in.model_dump(exclude_unset=True)
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
                setattr(current_status, field, value)
        for field, value in extra_data.items():
            setattr(current_status, field, value)
        session.add(current_status)
        await session.commit()
        await session.refresh(current_status)
        return to_incidence_status_out(status_in=current_status)
    except SQLAlchemyError as err:
        await session.rollback()
        return None
    
async def delete_incidence_status_by_id(
        *, session: AsyncSession, id= int
    ) -> Optional[Message]:
    try:
        query = (
            select(IncidenceStatus).where(IncidenceStatus.id == id).limit(1)
        )
        incidence_status: IncidenceStatus = await session.scalar(query)
        if not incidence_status:
            return Message(
                message= "incident status not removed"
            )
        await session.delete(incidence_status)
        await session.commit()
        return Message(
            message= "incident status removed"
        )
    except SQLAlchemyError as err:
        await session.rollback()
        return Message(
            message="incident status not removed"
        )
    
async def validate_incidence_status_exists(
        *, session: AsyncSession, id: int
    ) -> bool:
    return bool(await get_incidence_status__by_id(session=session, id=id))