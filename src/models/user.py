from datetime import date
from typing import Annotated, List, Optional
from pydantic import BaseModel, BeforeValidator, EmailStr, Field

from src.models.appointment import Appointment

PyObjectId = Annotated[str, BeforeValidator(str)]

class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    firstName: str
    lastName: str
    dateOfBirth: date
    email: EmailStr
    clalitUserCode: str
    clalitPassword: str
    appointments: List[Appointment]
    createdAt: date
    updatedAt: date
