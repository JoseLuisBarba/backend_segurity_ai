from fastapi import APIRouter
from app.api.routes import (
    incidence, login, user, role, citizen, 
    incidence_type, incidence_status, email
)

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, prefix='/users', tags=["users"])
api_router.include_router(role.router, prefix='/role', tags=["role"])
api_router.include_router(citizen.router, prefix='/citizen', tags=["citizen"])
api_router.include_router(incidence.router, prefix='/incidence', tags=['incidence'])
api_router.include_router(incidence_status.router, prefix='/incidence-status', tags=['incidence-status'])
api_router.include_router(incidence_type.router, prefix='/incidence-type', tags=['incidence-type'])
api_router.include_router(email.router, prefix='/email', tags=['email'])

