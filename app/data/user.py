
from app.core.segurity import get_password_hash, verify_password
from app.core.config import settings
from app.model.orm import User
from app.dto.user import UserCreate, UserUpdate, UserPublic, UsersPublic
from app.helpers.convertions import make_naive
from app.helpers.user import to_user_out
from app.dto.utils import Message
from app.api.deps import SessionDep

from typing import Optional
from sqlalchemy.sql import select
from datetime import datetime, timezone
from datetime import date
from sqlalchemy.sql import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException, status


import logging

logger = logging.getLogger(__name__)


async def get_users(
        *, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> Optional[UserPublic]:
    count_query = (
        select(func.count()).select_from(User).offset(skip).limit(limit)
    )
    response = await session.scalar(count_query)
    user_count = int(response)
    users_query = (
        select(User).offset(skip).limit(limit)
    )
    users: list[User] = await session.scalars(users_query)
    users_out: list[UserPublic] = [ 
        to_user_out(user_in=user_data) for user_data in users
    ]
    return UsersPublic(data=users_out, count=user_count)

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

async def get_user_by_id(
        *, session: AsyncSession, id: str    
    ) -> Optional[User]:
    query = (
        select(User).where(User.id == id).limit(1)
    ) 
    user: User = await session.scalar(query) 
    return user

async def validate_user_exists(
        *, session: AsyncSession, id: str
    ) -> bool:
    return bool(await get_user_by_id(session=session, id=id))

async def authenticate(
        *, session: AsyncSession, email: str, password: str
    ) -> Optional[User]:
    
    db_user: User = await get_user_by_email(session= session, email=email)
    if not db_user:
        return None 
    if not verify_password(password, db_user.hashed_password):
        return None 
    return db_user
        
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


async def update_user(
        *, session: AsyncSession, current_user: User ,user_in: UserUpdate
    ) -> Optional[User]:
    try:
        update_data = user_in.model_dump(exclude_unset=True)
        extra_data = {}
        extra_data["updatedAt"] = make_naive(datetime.now(timezone.utc))
        if "is_active" in update_data:
            if not bool(update_data["is_active"]):
                update_data["is_active"] = False
                extra_data["deletedAt"] = make_naive(datetime.now(timezone.utc))
            else:
                extra_data["deletedAt"] = None
        if "password" in update_data:
            if update_data["password"] is not None:
                password = update_data["password"]
                hashed_password = get_password_hash(password=password)
                extra_data["hashed_password"] = hashed_password
        for field, value in update_data.items():
            if value is not None:
                setattr(current_user, field, value)
        for field, value in extra_data.items():
            setattr(current_user, field, value)
        session.add(current_user)
        await session.commit()
        await session.refresh(current_user)
        return current_user
    except SQLAlchemyError as err:
        await session.rollback()
        return None
    except ValidationError as err:
        print(f"Validation error: {str(err)}")
        return None
    except Exception as err:
        await session.rollback()
        print(f"Unexpected error: {str(err)}")
        return None

    
async def delete_user_by_id(
        *, session: AsyncSession, id= str
    ) -> Optional[Message]:
    try:
        query = (
            select(User).where(User.id == id).limit(1)
        )
        user: User = await session.scalar(query)
        if not User:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No user found with ID: {id}"
            )
        await session.delete(user)
        await session.commit()
        return Message(
            message="user deleted"
        )
    except HTTPException as e:
        raise e
    except SQLAlchemyError as err:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user due to a database error: {str(err)}"
        )
    except Exception as err:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(err)}"
        )


# Función auxiliar
async def update_user_status(
        session: SessionDep, user_id: int, is_active: bool
    ) -> Optional[UserPublic]:

    try:
        current_user: User = await session.get(User, user_id)
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No user found with ID: {user_id}"
            )
        user_in: UserUpdate = UserUpdate(is_active=is_active)
        current_user: User = await update_user(
            session=session, current_user=current_user, user_in=user_in
        )
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update the user with ID: {user_id}."
            )
        return current_user
    except HTTPException as e:
        raise e
    except (SQLAlchemyError, IntegrityError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {str(e)}"
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )