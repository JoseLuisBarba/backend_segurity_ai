from app.model.orm import Role
from app.dto.role import RoleOut

def to_role_out(role_in: Role)->RoleOut:
    return RoleOut(
        id= role_in.id, 
        name= role_in.name, 
        description= role_in.description, 
        is_active= role_in.is_active, 
        createdAt= role_in.createdAt, 
        updatedAt= role_in.updatedAt,
        deletedAt= role_in.deletedAt
    )