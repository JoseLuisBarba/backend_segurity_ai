from typing import Optional  
from fastapi import APIRouter, Depends, HTTPException, status

from app.model.orm import IncidenceType
from app.api.deps import (
    CurrentUser, SessionDep, get_current_active_superuser, get_current_user
)
from app.data.incidence_type import (
    get_incidences_type, create_incidence_type, get_incidence_type_by_name,
    update_incidence_type, get_incidence_type_id, delete_incidence_type_by_id
)
from app.data.user import (
    validate_user_exists
) 
from app.dto.incidence_type import (
    IncidenceTypeOut, IncidenceTypesOut, IncidenceTypeCreate, 
    IncidenceTypeUpdate
)
from app.dto.utils import Message

router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=IncidenceTypesOut,
)
async def sweb_read_incidence_types(session: SessionDep, skip: int = 0, limit: int = 100) -> Optional[IncidenceTypesOut]:
    """
    Retrieve Incidence Types.
    """
    try:
        types_out: IncidenceTypesOut = await get_incidences_type(session=session, skip=skip, limit=limit)
        if not types_out:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="could not get incidence types.",
            )
        return types_out
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="could not get incidence types.",
        )

@router.get("/{type_id}", dependencies=[Depends(get_current_user)], response_model=IncidenceTypeOut)
async def sweb_read_incidence_type_by_id(
       type_id: int ,session: SessionDep
    ) -> Optional[IncidenceTypeOut]:
    """Get a specific Incidence type by id
    """
    try:
        type_out: IncidenceTypeOut = await get_incidence_type_id(session=session, type_id=type_id)
        if not type_out:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Incidence type not found.",
            )
        return type_out
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incidence type not found.",
        ) 

@router.post(
    "/create", dependencies=[Depends(get_current_active_superuser)], response_model=IncidenceTypeOut
)
async def sweb_create_incidence_type(*, session: SessionDep, type_create: IncidenceTypeCreate) -> Optional[IncidenceTypeOut]:
    try:
        if not (await validate_user_exists(session=session, id=type_create.user_id)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user id does not exist.",
            )
        type_out: IncidenceTypeOut = await create_incidence_type(session=session, incidence_type_create=type_create)
        if not type_out:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The incidence type could not be created.",
            )
        return type_out
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The incidence type could not be created.",
        )
    
@router.patch(
    "/modify/{type_id}", dependencies=[Depends(get_current_active_superuser)],
    response_model=IncidenceTypeOut
)
async def sweb_update_incidence_type(
        *, session: SessionDep, type_id: int, type_in: IncidenceTypeUpdate
    ) -> Optional[IncidenceTypeOut]:
    """update incidence type
    """
    try:
        current_type: IncidenceType = await session.get(IncidenceType, type_id)
        if not current_type:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="IncidenceType with this id not exists."
            )
        new_type: IncidenceTypeOut = await update_incidence_type(
            session=session, current_type=current_type, type_in=type_in
        )
        if not new_type:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="Failed to update incidence type"
            )
        return new_type
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update incidence type",
        )
    
@router.patch(
    "/remove/{type_id}", dependencies=[Depends(get_current_active_superuser)],
    response_model=IncidenceTypeOut
)
async def sweb_remove_incidence_type(
        *, session: SessionDep, type_id: int
    ) -> Optional[IncidenceTypeOut]:

    try:
        current_type: IncidenceType = await session.get(IncidenceType, type_id)
        if not current_type:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="IncidenceType with this id not exists."
            )
        type_in: IncidenceTypeUpdate = IncidenceTypeUpdate(
            is_active= False
        )
        update_type: IncidenceTypeOut = await update_incidence_type(
            session=session, current_type=current_type, type_in=type_in
        )
        if not update_type:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="Failed to remove incidence type"
            )
        return update_type
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to remove incidence type",
        )
    
@router.patch(
    "/activate/{type_id}", dependencies=[Depends(get_current_active_superuser)],
    response_model=IncidenceTypeOut
)
async def sweb_activate_incidence_type(
        *, session: SessionDep, type_id: int
    ) -> Optional[IncidenceTypeOut]:

    try:
        current_type: IncidenceType = await session.get(IncidenceType, type_id)
        if not current_type:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="IncidenceType with this id not exists."
            )
        type_in: IncidenceTypeUpdate = IncidenceTypeUpdate(
            is_active= True
        )
        update_type: IncidenceTypeOut = await update_incidence_type(
            session=session, current_type=current_type, type_in=type_in
        )
        if not update_type:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="Incident type could not be activated"
            )
        return update_type
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incident type could not be activated",
        )
    
@router.delete(
    "/delete/{type_id}", dependencies=[Depends(get_current_active_superuser)],
    response_model=Message
)
async def sweb_delete_incidence_type(
        *, session: SessionDep, type_id: int
    ) -> Optional[Message]:

    try:
        current_type: IncidenceType = await session.get(IncidenceType, type_id)
        if not current_type:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="IncidenceType with this id not exists."
            )
        message: Message = await delete_incidence_type_by_id(session=session, type_id= type_id)
        if not message:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="Failed to delete incidence type"
            )
        return message
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete incidence type",
        )