from app.api.deps import (
    CurrentUser, SessionDep, get_current_active_superuser, get_current_user
)
from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List

class EmailSchema(BaseModel):
    email: List[EmailStr]


router = APIRouter()

