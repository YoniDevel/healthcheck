from datetime import date
from typing import List, Annotated, Optional
from pydantic import Field, BaseModel, EmailStr
from pydantic.functional_validators import BeforeValidator

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
