from datetime import date
from geojson import Point
from pydantic import BaseModel, PositiveInt

class Visit(BaseModel):
    date: date
    location: Point

class Appointment(BaseModel):
    name: str # To be replaced by an enum soon
    frequency: PositiveInt
    lastVisit: Visit
    nextVisit: Visit
 