from app.model.orm import Citizen
from app.dto.citizen import CitizenOut


def to_citizen_out(citizen_in: Citizen)->CitizenOut:
    citizen: CitizenOut = CitizenOut(
        dni= citizen_in.dni,
        firstname= citizen_in.firstname,
        lastname= citizen_in.lastname,
        fathername=citizen_in.fathername,
        mothername= citizen_in.mothername,
        birthdate= citizen_in.birthdate,
        img= citizen_in.img,
        address= citizen_in.address,
        telephone= citizen_in.telephone,
        cellphone= citizen_in.cellphone,
        email= citizen_in.email,
        is_active= citizen_in.is_active,
        createdAt= citizen_in.createdAt,
        updatedAt= citizen_in.updatedAt,
        deletedAt= citizen_in.deletedAt
    )
    return citizen