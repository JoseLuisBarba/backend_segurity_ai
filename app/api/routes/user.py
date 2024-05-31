from datetime import timedelta 
from typing import Annotated, Any, Optional  



from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse 
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.sql import select, update, func


from app.data.user import get_user_by_email, create
from app.api.deps import (
    CurrentUser, SessionDep, get_current_active_superuser
)
from app.core import segurity
from app.core.config import settings
from app.core.segurity import get_password_hash
from app.dto.utils import Message
from app.dto.auth import NewPassword, Token
from app.dto.user import UserPublic, UsersPublic, UserCreate, UserRegister
from app.model.orm import User
from app.helpers.user import map_create_no_superuser



router = APIRouter()

@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersPublic,
)
async def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve users.
    """

    count_query = (
        select(func.count()).select_from(User).limit(1)
    )
    response = await session.scalar(count_query)

    user_count = int(response)
    users_query = (
        select(User).offset(skip).limit(limit)
    )
    users: list[User] = await session.scalars(users_query)

    users_public: list[UserPublic] = [
        UserPublic(
            id= user_data.id
        ) for user_data in users
    ]

    return UsersPublic(data=users_public, count=user_count)


@router.post(
    "/create", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic
)
async def create_user(*, session: SessionDep, user_in: UserCreate) -> Optional[User]:
    user: User = await get_user_by_email(
        session= session, email= user_in.email
    )
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )
    user = await create(session=session, user_create= user_in)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user could not be created.",
        )
    
    return user
    

@router.get("/me", response_model= UserPublic)
async def read_user_me(current_user: CurrentUser) -> UserPublic:
    """ Get current user.
    """
    return current_user


@router.post("/signup", response_model=UserPublic)
async def register_user(
        session: SessionDep, user_in: UserRegister
    ) -> UserPublic:
    try:
        #check if user already exists
        user: User = await get_user_by_email(
            session= session, email= user_in.email
        )

        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user with this email already exists in the system",
            )
        
        user_create = map_create_no_superuser(user_register=user_in)
        
        user_created = await create(session=session, user_create=user_create)

        if not user_created:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user could not be created.",
            )
        return user_created
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e,
        )
    
@router.get("/{user_id}", response_model=UserPublic)
async def read_user_by_id(
       user_id: int ,session: SessionDep, current_user: CurrentUser
    ) -> Any:
    """Get a specific user by id
    """
    try:
        user: User = await session.get(User, user_id)
        if user == current_user:
            return user
        if not current_user.is_superuser:
            raise HTTPException(
                status_code= status.HTTP_403_FORBIDDEN,
                detail="The user doesn't have enough privileges",
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e,
        )