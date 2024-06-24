from typing import Optional  
from fastapi import APIRouter, Depends, HTTPException, status
from app.model.orm import IncidenceStatus
from app.api.deps import (
    CurrentUser, SessionDep, get_current_active_superuser, get_current_user
)
from app.data.incidence_status import (
    get_incidence_status__by_id, get_incidence_status_by_name, create_incidence_status, 
    update_incidence_status, delete_incidence_status_by_id, get_incidences_status
)
from app.data.user import (
    validate_user_exists
) 
from app.dto.incidence_status import (
    IncidenceStatusCreate, IncidenceStatusOut, IncidenceStatusUpdate, ListStatusOut
)
from app.dto.utils import Message

router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=IncidenceStatusOut,
)
async def sweb_read_incidences_status(
        session: SessionDep, skip: int = 0, limit: int = 100
    ) -> Optional[IncidenceStatusOut]:
    """
    Retrieve Incidence status.
    """
    try:
        status_out: IncidenceStatusOut = await get_incidences_status(
            session=session, skip=skip, limit=limit
        )
        if not status_out:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="could not get incidence status.",
            )
        return status_out
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="could not get incidence status.",
        )

@router.get("/{status_id}", dependencies=[Depends(get_current_user)], response_model=IncidenceStatusOut)
async def sweb_read_incidence_status_by_id(
       status_id: int ,session: SessionDep
    ) -> Optional[IncidenceStatusOut]:
    try:
        status_out: IncidenceStatusOut = await get_incidence_status__by_id(session=session, id=status_id)
        if not status_out:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Incidence status not found.",
            )
        return status_out
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incidence status not found.",
        ) 

@router.post(
    "/create", dependencies=[Depends(get_current_active_superuser)], response_model=IncidenceStatusOut
)
async def sweb_create_incidence_status( *, 
        session: SessionDep, status_create: IncidenceStatusCreate
    ) -> Optional[IncidenceStatusOut]:
    try:
        if not (await validate_user_exists(session=session, id=status_create.user_id)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user id does not exist.",
            )
        status_out: IncidenceStatusOut = await create_incidence_status(
            session=session, status_create=status_create
        )
        if not status_out:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The incidence status could not be created.",
            )
        return status_out
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The incidence status could not be created.",
        )
    
@router.patch(
    "/modify/{status_id}", dependencies=[Depends(get_current_active_superuser)],
    response_model=IncidenceStatusOut
)
async def sweb_update_incidence_status( 
        session: SessionDep, type_id: int, status_in: IncidenceStatusUpdate
    ) -> Optional[IncidenceStatusOut]:

    try:
        current_status: IncidenceStatus = await session.get(IncidenceStatus, type_id)
        if not current_status:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="Incidence status with this id not exists."
            )
        new_status: IncidenceStatusOut = await update_incidence_status(
            session=session, current_status=current_status, status_in=status_in
        )
        if not new_status:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="Failed to update incidence status"
            )
        return new_status
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update incidence status",
        )
    
@router.patch(
    "/remove/{status_id}", dependencies=[Depends(get_current_active_superuser)],
    response_model=IncidenceStatusOut
)
async def sweb_remove_incidence_status( 
        session: SessionDep, status_id: int 
    ) -> Optional[IncidenceStatusOut]:

    try:
        current_status: IncidenceStatus = await session.get(IncidenceStatus, status_id)
        if not current_status:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="IncidenceType with this id not exists."
            )
        status_in: IncidenceStatusUpdate = IncidenceStatusUpdate(
            is_active=False
        )
        update_status: IncidenceStatusOut = await update_incidence_status(
            session=session, current_status=current_status, status_in=status_in
        )
        if not update_status:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="Failed to remove incidence status"
            )
        return update_status
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to remove incidence status",
        )
    
@router.patch(
    "/activate/{status_id}", dependencies=[Depends(get_current_active_superuser)],
    response_model=IncidenceStatusOut
)
async def sweb_activate_incidence_status(
        session: SessionDep, status_id: int
    ) -> Optional[IncidenceStatusOut]:

    try:
        current_status: IncidenceStatus = await session.get(IncidenceStatus, status_id)
        if not current_status:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="Incidence status with this id not exists."
            )
        status_in: IncidenceStatusUpdate = IncidenceStatusUpdate(
            is_active= True
        )
        update_status: IncidenceStatusOut = await update_incidence_status(
            session=session, current_status=current_status, status_in=status_in
        )
        if not update_status:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="Incident status could not be activated"
            )
        return update_status
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incident status could not be activated",
        )
    
@router.delete(
    "/delete/{status_id}", dependencies=[Depends(get_current_active_superuser)],
    response_model=Message
)
async def sweb_delete_incidence_status(
        session: SessionDep, status_id: int
    ) -> Optional[Message]:
    try:
        current_status: IncidenceStatus = await session.get(IncidenceStatus, status_id)
        if not current_status:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="Incidence status with this id not exists."
            )
        message: Message = await delete_incidence_status_by_id( session=session, id=status_id)
        if not message:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="Failed to delete incidence status"
            )
        return message
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete incidence status",
        )