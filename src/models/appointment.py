from datetime import datetime
from pydantic import BaseModel, Field, PositiveInt

from .specialization import Specialization

class Visit(BaseModel):
    date: datetime
    city: str

class Appointment(BaseModel):
    specialization: Specialization
    frequency: PositiveInt = Field(description='The frequency of the appointment (every *frequency* days)')
    lastVisit: Visit
    nextVisit: Visit
