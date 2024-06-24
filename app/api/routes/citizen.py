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

@router.get(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=CitizensOut,
)
async def sweb_read_citizens(session: SessionDep, skip: int = 0, limit: int = 100) -> Optional[CitizensOut]:
    """
    Retrieve citizens.
    """
    try:
        citizens_out: CitizensOut = await get_citizens(session=session, skip=skip, limit=limit)
        if not citizens_out:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="could not get citizens.",
            )
        return citizens_out
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="could not get citizens.",
        )

@router.post(
    "/create", dependencies=[Depends(get_current_active_superuser)], response_model=CitizenOut
)
async def sweb_register_citizen(*, session: SessionDep, citizen_create: CitizenCreate) -> Optional[CitizenOut]:
    try:
        citizen_out: CitizenOut = await create_citizen(session=session, citizen_create= citizen_create)
        if not citizen_out:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The citizen could not be registered.",
            )
        return citizen_out
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The citizen could not be created.",
        )
    

@router.get("/{citizen_id}", dependencies=[Depends(get_current_user)], response_model=CitizenOut)
async def sweb_read_role_by_id(
       citizen_id: str ,session: SessionDep
    ) -> Optional[CitizenOut]:
    """Get a specific citizen_out by id
    """
    try:
        citizen_out: CitizenOut = await get_citizen_by_dni(session=session, citizen_dni=citizen_id)
        if not citizen_out:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Citizen not found.",
            )
        return citizen_out
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role not found.",
        )
    

