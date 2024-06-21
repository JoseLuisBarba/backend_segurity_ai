from typing import Optional
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.model.orm import Citizen
from app.dto.citizen import CitizenCreate, CitizenOut, CitizensOut

from datetime import datetime, timezone
from datetime import date
from sqlalchemy.sql import select, update, func


def make_naive(dt):
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt

def to_citizen_out(citizen_in: Citizen)->CitizenOut:
    citizen: CitizenOut = CitizenOut(
        dni= citizen_in.dni,
        firstname= citizen_in.firstname,
        lastname= citizen_in.lastname,
        fathername=citizen_in.fathername,
        mothername= citizen_in.mothername,
        birthdate= citizen_in.birthdate,
        img= citizen_in.img,
        address= citizen_in.address,
        telephone= citizen_in.telephone,
        cellphone= citizen_in.cellphone,
        email= citizen_in.email,
        is_active= citizen_in.is_active,
        createdAt= citizen_in.createdAt,
        updatedAt= citizen_in.updatedAt,
        deletedAt= citizen_in.deletedAt
    )
    return citizen

async def get_citizens(
        *, session: AsyncSession, skip: int = 0, limit: int = 100
    ):
    count_query = (
        select(func.count()).select_from(Citizen).where(Citizen.is_active == True).offset(skip).limit(limit)
    )
    response = await session.scalar(count_query)

    citizens_count = int(response)
    citizens_query = (
        select(Citizen).where(Citizen.is_active == True).offset(skip).limit(limit)
    )
    citizens: list[Citizen] = await session.scalars(citizens_query)

    citizens_out: list[CitizenOut] = [ 
        to_citizen_out(citizen_in=citizen_data) for citizen_data in citizens 
    ]

    return CitizensOut(data=citizens_out, count=citizens_count)

async def get_citizen_by_dni(
        *, session: AsyncSession, citizen_dni= str
    ) -> Optional[CitizenOut]:
    try:
        query = (
            select(Citizen).where(Citizen.dni == citizen_dni).limit(1)
        )
        citizen: Citizen = await session.scalar(query)
        if not citizen:
            return None
        return to_citizen_out(citizen_in=citizen)
    
    except SQLAlchemyError as err:
        return None
    


async def create_citizen(
        *, session: AsyncSession, citizen_create= CitizenCreate
    ) -> Optional[CitizenOut]:
    try:
        citizen_out: CitizenOut = await get_citizen_by_dni(
            session=session,
            citizen_dni= citizen_create.dni
        )
        if citizen_out:
            return None
        citizen_in: Citizen = Citizen(
            dni= citizen_create.dni,
            firstname= citizen_create.firstname,
            lastname= citizen_create.lastname,
            fathername= citizen_create.fathername,
            mothername= citizen_create.mothername,
            birthdate= citizen_create.birthdate,
            img= citizen_create.img,
            address= citizen_create.address,
            telephone= citizen_create.telephone,
            cellphone= citizen_create.cellphone,
            email= citizen_create.email,
            is_active= True,
            createdAt= make_naive(datetime.now(timezone.utc)),
            updatedAt= None,
            deletedAt= None
        )
        session.add(citizen_in)
        await session.commit()
        await session.refresh(citizen_in)
        if not citizen_in:
            return None

        return to_citizen_out(citizen_in=citizen_in)
    except SQLAlchemyError as err:
        await session.rollback()
        return None