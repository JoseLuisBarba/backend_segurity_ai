from fastapi import APIRouter
from app.api.routes import (
    login, user, role, citizen
)

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, prefix='/users', tags=["users"])
api_router.include_router(role.router, prefix='/role', tags=["role"])
api_router.include_router(citizen.router, prefix='/citizen', tags=["citizen"])