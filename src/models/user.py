from bson import ObjectId
from datetime import date
from pydantic import EmailStr
from typing import List, TypedDict, NotRequired

from src.models.appointment import Appointment

class User(TypedDict):
    _id: NotRequired[ObjectId]
    firstName: str
    lastName: str
    dateOfBirth: date
    email: EmailStr
    clalitUserCode: str
    clalitPassword: str
    appointments: List[Appointment]
    createdAt: date
    updatedAt: date
