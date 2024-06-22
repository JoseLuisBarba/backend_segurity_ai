from datetime import timedelta 
from typing import Annotated, Any, Optional  
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse 
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.sql import select, update, func


from app.data.user import (
    get_user_by_email, create, update_user, get_users
)
from app.api.deps import (
    CurrentUser, SessionDep, get_current_active_superuser
)
from app.core import segurity
from app.core.config import settings
from app.core.segurity import get_password_hash
from app.dto.utils import Message
from app.dto.auth import NewPassword, Token
from app.dto.user import UserPublic, UsersPublic, UserCreate, UserRegister, UserUpdate
from app.model.orm import User
from app.helpers.user import map_create_no_superuser, to_user_out



router = APIRouter()

@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersPublic,
)
async def sweb_read_users(
        session: SessionDep, skip: int = 0, limit: int = 100
    ) -> Optional[UsersPublic]:
    """
    Retrieve users.
    """
    try:
        users_out: UsersPublic = await get_users(session=session, skip=skip, limit=limit)
        if not users_out:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="could not get users.",
            )
        return users_out
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="could not get users.",
        )    

@router.post(
    "/create", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic
)
async def sweb_create_user(*, session: SessionDep, user_in: UserCreate) -> Optional[User]:
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
async def sweb_read_user_me(current_user: CurrentUser) -> UserPublic:
    """ Get current user.
    """
    return current_user


@router.post("/signup", response_model=UserPublic)
async def sweb_register_user(
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
async def sweb_read_user_by_id(
       user_id: str, session: SessionDep, current_user: CurrentUser
    ) -> Optional[UserPublic]:
    """Get a specific user by id
    """
    try:
        user: User = await session.get(User, user_id)

        if not user:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="The user could not be obtained",
            )

        if user == current_user:
            return user
        if not current_user.is_superuser:
            raise HTTPException(
                status_code= status.HTTP_403_FORBIDDEN,
                detail="The user doesn't have enough privileges",
            )
        return to_user_out(user_in=user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The user could not be obtained',
        )
    

@router.patch(
    "/{user_id}", dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic
)
async def sweb_update_user(*, session: SessionDep, user_id: str, user_in: UserUpdate) -> Any:
    """update user
    """
    try:
        db_user: User = await session.get(User, user_id)
        if not db_user:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="User with this email already exists"
            )
        
        if user_in.email:
            existing_user: User = await get_user_by_email(session=session, email=user_in.email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code= status.HTTP_409_CONFLICT,
                    detail="User with this email already exists"
                )
        db_user: User = await update_user(session=session, db_user=db_user, user_in=user_in)

        if not db_user:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="Failed to update user"
            )
        return db_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e,
        )
    

async def delete_user():
    pass 
    


