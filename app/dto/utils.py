from typing import Optional
from pydantic import BaseModel, EmailStr, Field 
from datetime import datetime
from datetime import date
from uuid import UUID

class Message(BaseModel):
    message: str