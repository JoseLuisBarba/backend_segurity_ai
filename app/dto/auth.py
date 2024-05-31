from typing import Optional
from pydantic import BaseModel


#JSON payload containing access token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Contents of JWT token
class TokenPayload(BaseModel):
    sub:  Optional[str] # user id

class NewPassword(BaseModel):
    token: str 
    new_password: str