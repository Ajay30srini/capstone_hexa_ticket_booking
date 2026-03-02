from datetime import datetime
from pydantic import BaseModel, Field

class BookingHoldIn(BaseModel):
    event_id: int
    seat_numbers: list[str] = Field(min_length=1)

class BookingOut(BaseModel):
    id: int
    user_id: int
    event_id: int
    status: str
    seat_numbers: list[str]
    created_at: datetime
    confirmed_at: datetime | None = None
    cancelled_at: datetime | None = None

    class Config:
        from_attributes = True