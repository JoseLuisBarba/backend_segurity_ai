from typing import Optional  
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


from app.model.orm import Citizen
from app.api.deps import (
    SessionDep, get_current_active_superuser, get_current_user
)
from app.data.peru_data import apiNetPe
from app.dto.citizen import CitizenInfo

from app.dto.utils import Message

router = APIRouter()


@router.get(
    "/info-dni/{dni}",
    dependencies=[Depends(get_current_user)],
    response_model=CitizenInfo,
)
async def web_service_read_person_with_dni(*, session: SessionDep, dni: str="") -> Optional[CitizenInfo]:
    try:
        citizen_info: Optional[CitizenInfo] = apiNetPe.get_person(dni=dni)
        if not citizen_info:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while the citizen info was being searched",
            )
        return citizen_info
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while the citizen info was being searched",
        )