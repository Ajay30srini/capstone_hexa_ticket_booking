from datetime import datetime
from pydantic import BaseModel, Field


class EventCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    venue: str = Field(min_length=2, max_length=200)
    date: datetime
    total_seats: int = Field(ge=1, le=5000)


class EventStatusUpdate(BaseModel):
    status: str = Field(pattern="^(draft|published|cancelled)$")


class EventOut(BaseModel):
    id: int
    title: str
    venue: str
    date: datetime
    total_seats: int
    organizer_id: int
    status: str

    class Config:
        from_attributes = True