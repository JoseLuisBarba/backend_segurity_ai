from app.dto.user import UserCreate, UserRegister



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