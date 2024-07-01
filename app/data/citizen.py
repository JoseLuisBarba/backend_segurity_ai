from app.model.orm import Citizen
from app.dto.citizen import CitizenCreate, CitizenOut, CitizensOut
from app.helpers.convertions import make_naive
from app.helpers.citizen import to_citizen_out
from app.dto.utils import Message

from datetime import datetime, timezone
from sqlalchemy.sql import select, func
from typing import Optional
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError




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
    

async def delete_citizen_by_id(
        *, session: AsyncSession, id= str
    ) -> Optional[Message]:
    try:
        query = (
            select(Citizen).where(Citizen.dni == id).limit(1)
        )
        result = await session.execute(query)
        citizen = result.scalars().one_or_none()

        if citizen is None:
            return Message(
                message= f"The citizen with ID {id} was not removed"
            )
        await session.delete(citizen)
        await session.commit()
        return Message(
            message= f"The citizen with ID {id} was removed"
        )
    except SQLAlchemyError as err:
        await session.rollback()
        return Message(
            message="The citizen was not removed"
        )