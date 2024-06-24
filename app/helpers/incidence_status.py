from app.model.orm import IncidenceStatus
from app.dto.incidence_status import IncidenceStatusOut

def to_incidence_status_out(status_in: IncidenceStatus)->IncidenceStatusOut:
    status_out = IncidenceStatusOut(
        id= status_in.id,
        name= status_in.name,
        description= status_in.description,
        user_id= status_in.user_id,
        is_active= status_in.is_active,
        createdAt= status_in.createdAt,
        updatedAt= status_in.updatedAt,
        deletedAt= status_in.deletedAt
    )
    return status_out