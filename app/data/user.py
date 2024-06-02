from typing import Any, Optional
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import model_validator
from app.core.segurity import get_password_hash, verify_password
from app.core.config import settings
from app.model.orm import User
from app.dto.user import UserCreate, UserUpdate

from datetime import datetime, timezone
from datetime import date

import logging

logger = logging.getLogger(__name__)


def make_naive(dt):
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt

async def create(
        *, session: AsyncSession, user_create: UserCreate
    ) -> Optional[User]:
    try:
        user = User(
            id= user_create.id,
            email = user_create.email,
            hashed_password= get_password_hash(user_create.password),
            is_superuser= user_create.is_superuser,
            name= user_create.name,
            lastname= user_create.lastname,
            phone= user_create.phone,
            birthdate= user_create.birthdate,
            img= None, 
            is_active= True,
            createdAt= make_naive(datetime.now(timezone.utc)),
            updatedAt = None,
            deletedAt= None
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        
        return user
    except Exception as err:
        await session.rollback()
        raise err

async def get_user_by_email(
        *, session: AsyncSession, email: str
    ) -> Optional[User]:
    query = (
        select(User).where(User.email == email).limit(1)
    )
    user : User = await session.scalar(query)
    return user


async def authenticate(
        *, session: AsyncSession, email: str, password: str
    ) -> Optional[User]:
    
    db_user: User = await get_user_by_email(session= session, email=email)
    if not db_user:
        return None 
    if not verify_password(password, db_user.hashed_password):
        return None 
    return db_user
        

async def update_user(
        *, session: AsyncSession, db_user: User, user_in: UserUpdate
    ) -> Optional[User]:  # Changed this line
    try:
        pass
    except Exception as err:
        await session.rollback()
        raise err  

async def init_db(
        *, session: AsyncSession
    ) -> None:
    query = (
        select(User).where(User.email == settings.FIRST_SUPERUSER).limit(1)
    )
    user: User = await session.scalar(query)
    if not user:
        user_in: UserCreate = UserCreate(
            id= '70659591', 
            email= 'barba@gmail.com', 
            password= 'chibolochivazo', 
            is_superuser= True, 
            name= 'master', 
            lastname= 'clover', 
            phone= '986798890', 
            birthdate= date.today()
        )
        user: User = await create(session=session, user_create=user_in)

