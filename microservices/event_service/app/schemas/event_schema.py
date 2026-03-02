from datetime import datetime
from pydantic import BaseModel, Field


class EventCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str | None = None
    venue: str | None = None
    event_date: datetime
    total_seats: int = Field(gt=0, le=5000)


class EventOut(BaseModel):
    id: int
    title: str
    description: str | None
    venue: str | None
    event_date: datetime
    total_seats: int
    organizer_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class EventStatusOut(BaseModel):
    id: int
    status: str

    class Config:
        from_attributes = True