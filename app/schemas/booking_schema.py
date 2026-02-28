from datetime import datetime
from pydantic import BaseModel, Field


class BookingCreate(BaseModel):
    event_id: int
    seat_numbers: list[str] = Field(min_length=1)


class BookingOut(BaseModel):
    id: int
    user_id: int
    event_id: int
    status: str
    created_at: datetime
    seat_numbers: list[str]

    class Config:
        from_attributes = True