from datetime import timedelta 
from typing import Annotated, Any  
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.db import async_session
from app.data.user import authenticate
from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.core import segurity
from app.core.config import settings
from app.core.segurity import get_password_hash
from app.dto.utils import Message
from app.dto.auth import NewPassword, Token
from app.dto.user import UserPublic
from app.model.orm import User

router = APIRouter()



@router.post("/login/access-token")
async def login_access_token(
        session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ) -> Token:
    """OAuth2 compatible token login, get an access token for future requests
    """
    try:
        user_db: User = await authenticate( 
            session=session, email=form_data.username, password=form_data.password
        )
        if not user_db:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password"
            )
        elif not user_db.is_active:
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= "Inactive user"
            )
        access_token_expire = timedelta(minutes= settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return Token(
            access_token= segurity.create_access_token(
                subject=user_db.id, 
                expires_delta=access_token_expire
            )
        )
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

@router.post("/login/test-token", response_model= UserPublic)
async def test_token(current_user: CurrentUser) -> Any:
    """Test access token
    """
    return current_user

