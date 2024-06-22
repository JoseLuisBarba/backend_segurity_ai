from app.dto.user import UserCreate, UserRegister, UserPublic
from app.model.orm import User


def map_create_no_superuser(user_register: UserRegister) -> UserCreate:
    return UserCreate(
        id=user_register.id,
        email=user_register.email,
        password=user_register.password,
        is_superuser=False,  
        name=user_register.name,
        lastname=user_register.lastname,
        phone=user_register.phone,
        birthdate=user_register.birthdate
    )

def to_user_out(user_in: User) -> UserPublic:
    return UserPublic(
        id= user_in.id,
        is_superuser= user_in.is_superuser,
        email= user_in.email,
        name= user_in.name,
        lastname= user_in.lastname,
        phone= user_in.phone,
        birthdate= user_in.birthdate,
        img= user_in.img,
        is_active= user_in.is_active,
        createdAt= user_in.createdAt,
        updatedAt= user_in.updatedAt,
        deletedAt= user_in.deletedAt
    )