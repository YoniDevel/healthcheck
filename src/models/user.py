from datetime import datetime
from typing import Annotated, List, Optional
from pydantic import Field, BaseModel, EmailStr, BeforeValidator, field_validator

from .appointment import Appointment
from ..utils import logger, calc_control_digit

PyObjectId = Annotated[str, BeforeValidator(str)]

class ClalitDetails(BaseModel):
    userCode: str
    password: str

class User(BaseModel):
    id: str = Field(pattern=r'^\d{2,9}$', alias='_id')
    firstName: str
    lastName: str
    dateOfBirth: datetime
    email: EmailStr
    clalitUserCode: str
    clalitPassword: str
    appointments: List[Appointment] = Field(default=[])
    cityOfResidence: str
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    @field_validator('_id', check_fields=False)
    @classmethod
    def validate_id_control_digit(cls, _id: str) -> str:
        control_digit = calc_control_digit(_id)
        if (control_digit != _id[8]):
            logger.error(f'Control digit for id {_id} is not correct')
            raise ValueError(f'Control digit for id {_id} is not correct')
        return _id
