from app.model.orm import IncidenceType
from app.dto.incidence_type import IncidenceTypeOut


def to_incidence_type_out(type_in: IncidenceType)->IncidenceTypeOut:
    type = IncidenceTypeOut(
        id= type_in.id,
        name= type_in.name,
        description= type_in.description,
        user_id= type_in.user_id,
        is_active= type_in.is_active,
        createdAt= type_in.createdAt,
        updatedAt= type_in.updatedAt,
        deletedAt= type_in.deletedAt
    )
    return type