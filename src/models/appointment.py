from datetime import datetime
from pydantic import BaseModel, Field, PositiveInt

class Visit(BaseModel):
    date: datetime
    city: str

class Appointment(BaseModel):
    name: str # To be replaced by an enum soon
    frequency: PositiveInt = Field(description='The frequency of the appointment (every *frequency* days)')
    lastVisit: Visit
    nextVisit: Visit
