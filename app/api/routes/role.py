from datetime import timedelta 
from typing import Annotated, Any, Optional  



from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse 
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.sql import select, update, func


from app.data.role import (
    create_role, get_role_by_id, get_roles
)
from app.api.deps import (
    CurrentUser, SessionDep, get_current_active_superuser, get_current_user
)
from app.core import segurity
from app.core.config import settings
from app.core.segurity import get_password_hash
from app.dto.utils import Message
from app.dto.auth import NewPassword, Token
from app.dto.user import UserPublic, UsersPublic, UserCreate, UserRegister, UserUpdate
from app.dto.role import RoleCreate, RoleOut, RolesOut
from app.model.orm import User
from app.helpers.user import map_create_no_superuser

router = APIRouter()



@router.get(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=RolesOut,
)
async def sweb_read_roles(session: SessionDep, skip: int = 0, limit: int = 100) -> Optional[RolesOut]:
    """
    Retrieve roles.
    """
    try:
        roles_out: RolesOut = await get_roles(session=session, skip=skip, limit=limit)
        if not roles_out:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="could not get roles.",
            )
        return roles_out
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="could not get roles.",
        )

@router.post(
    "/create", dependencies=[Depends(get_current_active_superuser)], response_model=RoleOut
)
async def sweb_create_role(*, session: SessionDep, role_create: RoleCreate) -> Optional[RoleOut]:
    try:
        role_out: RoleOut = await create_role(session=session, role_create= role_create)
        if not role_out:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The role could not be created.",
            )
        return role_out
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The role could not be created.",
        )

@router.get("/{role_id}", dependencies=[Depends(get_current_user)], response_model=RoleOut)
async def sweb_read_role_by_id(
       role_id: int ,session: SessionDep
    ) -> Optional[RoleOut]:
    """Get a specific role by id
    """
    try:
        role_out: RoleOut = await get_role_by_id(session=session, role_id=role_id)
        if not role_out:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found.",
            )
        return role_out
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role not found.",
        )
    

