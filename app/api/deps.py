import jwt

from collections.abc import AsyncGenerator
from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError


from app.core.config import settings
from app.core.db import engine, async_session

from app.dto.auth import TokenPayload 
from app.model.orm import User 


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


async def get_db() -> AsyncGenerator[AsyncSession, None, None]:
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(
        session: SessionDep, token: TokenDep
    ) -> Optional[User]:
    try:
        pay_load = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**pay_load)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    user: User = await session.get(User, token_data.sub) #search by id
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"     
        )
    if not user.is_active:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
            
        )
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

async def get_current_active_superuser(current_user: CurrentUser) -> Optional[User]:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user 