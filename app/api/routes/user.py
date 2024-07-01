from typing import Optional  
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


from app.data.user import (
    get_user_by_email, create,  get_users, delete_user_by_id, 
    update_user_status, update_user
)
from app.api.deps import (
    CurrentUser, SessionDep, get_current_active_superuser
)
from app.dto.utils import Message
from app.dto.user import (
    UserPublic, UsersPublic, UserCreate, UserRegister, UserUpdate
) 
from app.model.orm import User
from app.helpers.user import map_create_no_superuser, to_user_out



router = APIRouter()

@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersPublic,
)
async def web_service_read_users(
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
async def web_service_create_user(*, session: SessionDep, user_in: UserCreate) -> Optional[User]:
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
async def web_service_read_user_me(current_user: CurrentUser) -> UserPublic:
    """ Get current user.
    """
    return current_user


@router.post("/signup", response_model=UserPublic)
async def web_service_register_user(
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
async def web_service_read_user_by_id(
       user_id: str, session: SessionDep, current_user: CurrentUser
    ) -> Optional[UserPublic]:
    """Get a specific user by id
    """
    try:
        user: User = await session.get(User, user_id)

        if not user:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail=f"No user found with ID: {user_id}"
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
async def web_service_update_user(
        *, session: SessionDep, user_id: str, user_in: UserUpdate
    ) -> Optional[UserPublic]:

    try:
        current_user: User = await session.get(User, user_id)
        if not current_user:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail=f"No user found with ID: {user_id}"
            )
        if user_in.email:
            existing_user: User = await get_user_by_email(session=session, email=user_in.email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code= status.HTTP_409_CONFLICT,
                    detail=f"Another user with the email {user_in.email} already exists."
                )   
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
    
@router.patch(
    "/remove/{user_id}", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic
)
async def web_service_remove_user( *, session: SessionDep, user_id: int ) -> Optional[UserPublic]:
    return await update_user_status(session=session, user_id=user_id, is_active=False)


@router.patch(
    "/activate/{user_id}", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic
)
async def web_service_activate_user( *, session: SessionDep, user_id: int ) -> Optional[UserPublic]:
    return await update_user_status(session=session, user_id=user_id, is_active=True)


@router.delete(
    "/delete/{user_id}", dependencies=[Depends(get_current_active_superuser)],
    response_model=Message
)
async def web_service_delete_user(
        *, session: SessionDep, user_id: str
    ) -> Optional[Message]:

    try:
        current_user: User = await session.get(User, user_id)
        if not current_user:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail=f"No user found with ID: {user_id}"
            )
        message: Message = await delete_user_by_id(session=session, id=user_id)
        if not message:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete the user with ID: {user_id}."
            )
        return message
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


