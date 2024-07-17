from app.model.orm import Incidence
from app.dto.incidence import (
    IncidenceCreate, IncidenceOut, IncidencesOut, IncidenceCreateOut,
    IncidenceUpdate
)
from app.dto.utils import Message
from app.helpers.convertions import make_naive
from app.helpers.incidence import (
    to_incidence_out, to_incidence_create_out
)
from sqlalchemy.sql import select, update, func
from sqlalchemy.orm import joinedload
from typing import Optional
from sqlalchemy.sql import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
from pydantic import ValidationError



async def create_incidence(
        *, session: AsyncSession, incidence_create= IncidenceCreate
    ) -> Optional[IncidenceCreateOut]:
    try:
        incidence_in: Incidence = Incidence(
            description= incidence_create.description,
            type_id= incidence_create.type_id,
            status_id= incidence_create.status_id,
            user_id= incidence_create.user_id,
            citizen_id= incidence_create.citizen_id,
            longitude= incidence_create.longitude,
            latitude= incidence_create.latitude, 
            address= incidence_create.address,
            date_incident= incidence_create.date_incident,
            time_incident= incidence_create.time_incident,
            inciden_details= incidence_create.inciden_details,
            is_active= True,
            createdAt= make_naive(datetime.now(timezone.utc))
        )
        session.add(incidence_in)
        await session.commit()
        await session.refresh(incidence_in)
        if not incidence_in:
            return None
        return to_incidence_create_out(incidence_in=incidence_in)
    except SQLAlchemyError as err:
        await session.rollback()
        return None


async def get_incidence_by_id(
        *, session: AsyncSession, id= int
    ) -> Optional[IncidenceOut]:
    try:
        query = (
            select(Incidence)
            .where(Incidence.id == id)
            .limit(1)
            .options(
                joinedload(Incidence.type),
                joinedload(Incidence.status),
                joinedload(Incidence.citizen)
            )
        )
        result = await session.execute(query)
        incidence = result.scalars().one_or_none()
        if incidence is None:
            return None
        return to_incidence_out(incidence_in=incidence)
    except SQLAlchemyError as err:
        return None 
    

async def get_incidences(
        *, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> Optional[IncidencesOut]:
    count_query = (
        select(func.count())
        .select_from(Incidence)
        .where(Incidence.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    response = await session.scalar(count_query)
    incidence_count = int(response)
    incidence_query = (
        select(Incidence)
        .where(Incidence.is_active == True)
        .offset(skip)
        .limit(limit)
        .options(
            joinedload(Incidence.type),
            joinedload(Incidence.status),
            joinedload(Incidence.citizen)
        )
    )
    incidences = (await session.scalars(incidence_query)).all()
    incidences_out: list[IncidencesOut] = [ 
        to_incidence_out(incidence_in=incidence_data) for incidence_data in incidences
    ]
    return IncidencesOut(data=incidences_out, count=incidence_count)


async def validate_incidence_exists(
        *, session: AsyncSession, id: int
    ) -> bool:
    return bool(await get_incidence_by_id(session=session, id=id))



async def delete_incidence_by_id(
        *, session: AsyncSession, id= int
    ) -> Optional[Message]:
    try:
        query = (
            select(Incidence).where(Incidence.id == id).limit(1)
        )
        result = await session.execute(query)
        incidence = result.scalars().one_or_none()

        if incidence is None:
            return Message(
                message= "The incident was not removed"
            )
        await session.delete(incidence)
        await session.commit()
        return Message(
            message= "The incident was removed"
        )
    except SQLAlchemyError as err:
        await session.rollback()
        return Message(
            message="The incident was not removed"
        )
    
async def update_incidence(
        *, session: AsyncSession, current_incidence: Incidence ,incidence_in: IncidenceUpdate
    ) -> Optional[Incidence]: #check point
    try:
        update_data = incidence_in.model_dump(exclude_unset=True)
        extra_data = {}
        extra_data["updatedAt"] = make_naive(datetime.now(timezone.utc))
        if "is_active" in update_data: #chek
            if not bool(update_data["is_active"]):
                update_data["is_active"] = False
                extra_data["deletedAt"] = make_naive(datetime.now(timezone.utc))
            else:
                extra_data["deletedAt"] = None
        for field, value in update_data.items():
            if value is not None:
                setattr(current_incidence, field, value)
        for field, value in extra_data.items():
            setattr(current_incidence, field, value)
        session.add(current_incidence)
        await session.commit()
        await session.refresh(current_incidence)
        return current_incidence
    except SQLAlchemyError as err:
        await session.rollback()
        return None


async def update_incidence_availability(
        session: AsyncSession, incidence_id: int, is_active: bool
    ) -> Optional[Incidence]:
    try:
        current_incidence: Optional[Incidence] = await session.get(Incidence, incidence_id)
        if not current_incidence:
            return None
        incidence_in= IncidenceUpdate(is_active=is_active)
        current_incidence: Optional[Incidence] = await update_incidence(
            session=session, 
            current_incidence=current_incidence, 
            incidence_in=incidence_in
        )
        if not current_incidence:
            return None
        return current_incidence
    except SQLAlchemyError as err:
        await session.rollback()
        return None