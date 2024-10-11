from datetime import date
from pydantic import BaseModel, Field, PositiveInt

class Visit(BaseModel):
    date: date
    city: str

class Appointment(BaseModel):
    name: str # To be replaced by an enum soon
    frequency: PositiveInt = Field(description='The frequency of the appointment (every *frequency* days)')
    lastVisit: Visit
    nextVisit: Visit
