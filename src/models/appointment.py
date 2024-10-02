from datetime import date
from typing import TypedDict
from geojson import Point
from pydantic import BaseModel, PositiveInt, TypeAdapter

class Visit(BaseModel):
    date: date
    location: int

class Appointment(BaseModel):
    name: str # To be replaced by an enum soon
    frequency: PositiveInt
    lastVisit: Visit
    nextVisit: Visit
