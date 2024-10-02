from datetime import date
from typing import TypedDict
from geojson import Point
from pydantic import BaseModel, PositiveInt, TypeAdapter

class Visit(TypedDict):
    date: date
    location: int

class Appointment(TypedDict):
    name: str # To be replaced by an enum soon
    frequency: PositiveInt
    lastVisit: Visit
    nextVisit: Visit
