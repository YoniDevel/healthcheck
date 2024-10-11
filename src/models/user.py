import logging
from datetime import date
from typing import Annotated, List, Optional
from pydantic import Field, BaseModel, EmailStr, BeforeValidator, field_validator

from src.models.appointment import Appointment
from src.utils.control_digit import calc_control_digit

PyObjectId = Annotated[str, BeforeValidator(str)]

class ClalitDetails(BaseModel):
    userCode: str
    password: str

class User(BaseModel):
    id: str = Field(pattern=r'^\d{2,9}$', alias='_id')
    firstName: str
    lastName: str
    dateOfBirth: date
    email: EmailStr
    clalitUserCode: str
    clalitPassword: str
    appointments: List[Appointment]
    createdAt: Optional[date]
    updatedAt: Optional[date]
    cityOfResidence: str

    @field_validator('_id', check_fields=False)
    @classmethod
    def validate_id_control_digit(cls, _id: str) -> str:
        control_digit = calc_control_digit(_id)
        if (control_digit != _id[8]):
            logging.error(f'Control digit for id {_id} is not correct')
            raise ValueError(f'Control digit for id {_id} is not correct')
        return _id
