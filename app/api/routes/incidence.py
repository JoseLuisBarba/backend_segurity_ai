from app.model.orm import Incidence
from app.data.incidence import (
    IncidenceCreate, IncidenceOut, IncidencesOut, IncidenceCreateOut,
    IncidenceUpdate
)
from app.api.deps import (
    CurrentUser, SessionDep, get_current_active_superuser, get_current_user
)
from app.dto.utils import Message
from app.data.user import validate_user_exists
from app.data.incidence_status import validate_incidence_status_exists
from app.data.incidence_type import validate_incidence_type_exists
from app.data.citizen import validate_citizen_exists
from app.data.incidence import (
    create_incidence, get_incidences, get_incidence_by_id, delete_incidence_by_id,
    update_incidence, update_incidence_availability
) 


from typing import Optional  
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=IncidencesOut,
)
async def web_service_read_incidences(
        *, session: SessionDep, skip: int = 0, limit: int = 100
    ) -> Optional[IncidencesOut]:
    """
    Retrieve Incidence Types.
    """
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
        incidences_out: IncidencesOut = await get_incidences(session=session, skip=skip, limit=limit)
        if not incidences_out:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while the incidents were being searched",
            )
        return incidences_out
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while the incidents were being searched",
        )

@router.get("/{incidence_id}", dependencies=[Depends(get_current_user)], response_model=IncidenceOut)
async def web_service_read_incidence_by_id(
       incidence_id: int ,session: SessionDep
    ) -> Optional[IncidenceOut]:
    try:
        if incidence_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The incidence_id parameter must be greater than 0.",
            )
        incidence_out: IncidenceOut = await get_incidence_by_id(session=session, id=incidence_id)
        if not incidence_out:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Incidence not found.",
            )
        return incidence_out
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while the incident was being searched",
        )


@router.post(
    "/create", dependencies=[Depends(get_current_user)], response_model=IncidenceCreateOut
)
async def web_service_create_incidence(
        *, session: SessionDep, incidence_create: IncidenceCreate
    ) -> Optional[IncidenceCreateOut]:
    try:
        if not (await validate_user_exists(session=session, id=incidence_create.user_id)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User ID {incidence_create.user_id} does not exist.",
            )
        if not (await validate_citizen_exists(session=session, id=incidence_create.citizen_id)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Citizen ID {incidence_create.citizen_id} does not exist.",
            )
        if not (await validate_incidence_type_exists(session=session, id=incidence_create.type_id)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incidence type does not exist.",
            )
        if not (await validate_incidence_status_exists(session=session, id=incidence_create.status_id)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incidence status does not exist.",
            )
        incidence_out: IncidenceCreateOut = await create_incidence(
            session=session, 
            incidence_create=incidence_create
        )
        if not incidence_out:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="The incidence could not be created.",
            )
        return incidence_out
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the incidence.",
        )
    

@router.delete(
    "/delete/{incidence_id}", dependencies=[Depends(get_current_active_superuser)],
    response_model=Message
)
async def web_service_delete_incidence_type(
        *, session: SessionDep, incidence_id: int
    ) -> Optional[Message]:

    try:
        if incidence_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The incidence_id parameter must be greater than 0.",
            )
        incidence: Incidence = await session.get(Incidence, incidence_id)
        if not incidence:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="Incidence with this id not exists."
            )
        message: Message = await delete_incidence_by_id(session=session, id=incidence_id)
        if not message:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="Failed to delete incidence"
            )
        return message
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while deleting the incidence.",
        )
    


@router.patch(
    "/modify/{incidence_id}", dependencies=[Depends(get_current_user)],
    response_model=IncidenceOut
)
async def web_service_update_incidence(
        *, session: SessionDep, incidence_id: int, incidence_in: IncidenceUpdate
    ) -> Optional[IncidenceOut]:

    try:
        current_incidence: Optional[Incidence] = await session.get(Incidence, incidence_id)
        if not current_incidence:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail=f"No incidence found with ID: {incidence_id}"
            )
        current_incidence: Optional[Incidence] = await update_incidence(
            session=session, current_incidence=current_incidence, incidence_in=incidence_in
        )
        if not current_incidence:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update the incidence with ID: {incidence_id}."
            )
        incidence_out: Optional[IncidenceOut] = await get_incidence_by_id(session=session, id=current_incidence.id)
        if not incidence_out:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Incidence with ID {current_incidence.id} not found.",
            )
        return incidence_out
    except HTTPException as e:
        raise e
    except (SQLAlchemyError, IntegrityError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {str(e)}"
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
    


@router.patch(
    "/activate/{incidence_id}", dependencies=[Depends(get_current_user)],
    response_model=IncidenceOut
)
async def web_service_remove_incidence( *, session: SessionDep, incidence_id: int) -> Optional[IncidenceOut]:
    try:
        incidence_updated= await update_incidence_availability(
            session=session, incidence_id=incidence_id, is_active=True
        )
        if not incidence_updated:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail=f"No incidence found with ID: {incidence_id} to update"
            )
        incidence_out= await get_incidence_by_id(session=session, id=incidence_updated.id)
        if not incidence_out:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Incidence with ID {incidence_updated.id} not found.",
            )
        return incidence_out
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.patch(
    "/remove/{incidence_id}", dependencies=[Depends(get_current_user)],
    response_model=IncidenceOut
)
async def web_service_activate_incidence( *, session: SessionDep, incidence_id: int) -> Optional[IncidenceOut]:
    try:
        incidence_updated= await update_incidence_availability(
            session=session, incidence_id=incidence_id, is_active=False
        )
        if not incidence_updated:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail=f"No incidence found with ID: {incidence_id} to update"
            )
        incidence_out= await get_incidence_by_id(session=session, id=incidence_updated.id)
        if not incidence_out:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Incidence with ID {incidence_updated.id} not found.",
            )
        return incidence_out
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )