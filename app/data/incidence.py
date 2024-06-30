from app.model.orm import Incidence
from app.dto.incidence import (
    IncidenceCreate, IncidenceOut, IncidencesOut, IncidenceCreateOut
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