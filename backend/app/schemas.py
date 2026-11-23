from pydantic import BaseModel, Field


class IncidentCreate(BaseModel):
    title: str = Field(min_length=2, max_length=160)
    disaster_type: str = Field(min_length=2, max_length=40)
    severity: str = "Moderate"
    description: str = Field(default="", max_length=1000)
    location: str = Field(min_length=2, max_length=200)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    contact: str = Field(default="", max_length=80)

class IncidentStatusUpdate(BaseModel):
    status: str
