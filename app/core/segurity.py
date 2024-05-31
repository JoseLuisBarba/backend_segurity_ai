from datetime import datetime, timedelta, timezone
from typing import Any, Optional
import jwt
from passlib.context import CryptContext



from app.core.config import settings



password_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto"
)


def create_access_token(
        subject:  Optional[str], 
        expires_delta: timedelta
    ) -> str:

    if expires_delta:
        expire_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expire_delta = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return password_context.hash(password)