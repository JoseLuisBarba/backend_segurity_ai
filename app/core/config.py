from typing import List
from dotenv import load_dotenv
from decouple import config
from pydantic import (
    AnyUrl,
    AnyHttpUrl,
    BeforeValidator,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self



class Settings(BaseSettings):
    PORT: int = config("PORT", cast=int)
    API_V1_STR: str = "/api/v1"
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast=str)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7   # 7 days
    HOST: str = config("HOST", cast=str)
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        f"http://0.0.0.0:8000",
        f"http://127.0.0.1:4200",
        f"http://localhost:4200"
    ]
    PROJECT_NAME: str = "securotyai"

    # Database
    SQLALCHEMY_DATABASE_URL: str = config("SQLALCHEMY_DATABASE_URL", cast=str)
    AWS_BUCKET_NAME: str = config("AWS_BUCKET_NAME", cast=str)
    AWS_BUCKET_REGION: str = config("AWS_BUCKET_REGION", cast=str)

    FIRST_SUPERUSER: str = 'admin'
    FIRST_SUPERUSER_PASSWORD: str = 'mibarba'

    OPENAI_KEY: str = ''

    # SMTP_TLS: bool = True
    # SMTP_SSL: bool = False
    # SMTP_PORT: int = 587
    # SMTP_HOST: str | None = None
    # SMTP_USER: str | None = None
    # SMTP_PASSWORD: str | None = None
    # # TODO: update type to EmailStr when sqlmodel supports it
    # EMAILS_FROM_EMAIL: str
    # EMAILS_FROM_NAME: str

    # class Config:
    #     case_sensitive = True

settings = Settings()