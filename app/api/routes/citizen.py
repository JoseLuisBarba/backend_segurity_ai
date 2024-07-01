from typing import Optional  
from fastapi import APIRouter, Depends, HTTPException, status

from app.model.orm import Citizen
from app.data.citizen import (
    create_citizen, get_citizen_by_dni, get_citizens, delete_citizen_by_id
)
from app.api.deps import (
    SessionDep, get_current_active_superuser, get_current_user
)
from app.dto.citizen import CitizenCreate, CitizenOut, CitizensOut
from app.dto.utils import Message

router = APIRouter()

@router.get(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=CitizensOut,
)
async def web_service_read_citizens(*, session: SessionDep, skip: int = 0, limit: int = 100) -> Optional[CitizensOut]:
    try:
        if skip < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The skip parameter must be greater than or equal to 0.",
            )
        if limit <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The limit parameter must be greater than 0.",
            )
        citizens_out: CitizensOut = await get_citizens(session=session, skip=skip, limit=limit)
        if not citizens_out:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while the users were being searched",
            )
        return citizens_out
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while the users were being searched",
        )
    

@router.post(
    "/create", dependencies=[Depends(get_current_user)], response_model=CitizenOut
)
async def web_service_create_citizen(
        *, session: SessionDep, citizen_create: CitizenCreate
    ) -> Optional[CitizenOut]:
    try:
        citizen_out: CitizenOut = await create_citizen(session=session, citizen_create= citizen_create)
        if not citizen_out:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="The citizen could not be created.",
            )
        return citizen_out
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the incidence.",
        )
   

@router.get("/{citizen_id}", dependencies=[Depends(get_current_user)], response_model=CitizenOut)
async def web_service_read_citizen_by_id(
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
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while the citizen was being searched",
        )


@router.delete(
    "/delete/{citizen_id}", dependencies=[Depends(get_current_active_superuser)],
    response_model=Message
)
async def web_service_delete_citizen(
        *, session: SessionDep, citizen_id: str
    ) -> Optional[Message]:

    try:
        citizen: Citizen = await session.get(Citizen, citizen_id)
        if not citizen:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="The citizen with this id not exists."
            )
        message: Message = await delete_citizen_by_id(session=session, id=citizen_id)
        if not message:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="Failed to delete the citizen"
            )
        return message
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while deleting the citizen.",
        )