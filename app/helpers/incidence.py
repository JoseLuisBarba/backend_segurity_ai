from app.model.orm import Incidence, IncidenceType, IncidenceStatus, Citizen
from app.dto.incidence import IncidenceOut, IncidenceTypeOut, IncidenceStatusOut, CitizenOut, IncidenceCreateOut


def to_incidence_create_out(incidence_in: Incidence)->IncidenceCreateOut:
    incidence = IncidenceCreateOut(
        id= incidence_in.id,
        description= incidence_in.description,
        type_id= incidence_in.type_id,
        status_id= incidence_in.status_id,
        user_id= incidence_in.user_id,
        citizen_id= incidence_in.citizen_id,
        longitude= incidence_in.longitude,
        latitude= incidence_in.latitude,
        address= incidence_in.address,
        date_incident= incidence_in.date_incident,
        time_incident= incidence_in.time_incident,
        inciden_details= incidence_in.inciden_details,
        is_active= incidence_in.is_active,
        createdAt= incidence_in.createdAt,
        updatedAt= incidence_in.updatedAt,
        deletedAt= incidence_in.deletedAt
    )
    return incidence



def to_incidence_out(incidence_in: Incidence) -> IncidenceOut:
    incidence = IncidenceOut(
        id=incidence_in.id,
        description=incidence_in.description,
        type=IncidenceTypeOut(
            id=incidence_in.type.id,
            name=incidence_in.type.name,
        ),
        status=IncidenceStatusOut(
            id=incidence_in.status.id,
            name=incidence_in.status.name,
        ),
        citizen=CitizenOut(
            dni=incidence_in.citizen.dni,
            firstname=incidence_in.citizen.firstname,
            lastname=incidence_in.citizen.lastname,
            fathername=incidence_in.citizen.fathername,
            mothername=incidence_in.citizen.mothername,
            birthdate=incidence_in.citizen.birthdate,
            img=incidence_in.citizen.img,
            address=incidence_in.citizen.address,
            telephone=incidence_in.citizen.telephone,
            cellphone=incidence_in.citizen.cellphone,
            email=incidence_in.citizen.email
        ),
        longitude=incidence_in.longitude,
        latitude=incidence_in.latitude,
        address=incidence_in.address,
        date_incident=incidence_in.date_incident,
        time_incident=incidence_in.time_incident,
        inciden_details=incidence_in.inciden_details,
        is_active=incidence_in.is_active,
        createdAt=incidence_in.createdAt,
        updatedAt=incidence_in.updatedAt,
        deletedAt=incidence_in.deletedAt
    )
    return incidence