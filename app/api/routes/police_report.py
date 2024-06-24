from typing import Optional  
from fastapi import APIRouter, Depends, HTTPException, status
from app.data.citizen import (
    create_citizen, get_citizen_by_dni, get_citizens
)
from app.api.deps import (
    CurrentUser, SessionDep, get_current_active_superuser, get_current_user
)
from app.core.config import settings
from app.dto.citizen import CitizenCreate, CitizenOut, CitizensOut


router = APIRouter()


