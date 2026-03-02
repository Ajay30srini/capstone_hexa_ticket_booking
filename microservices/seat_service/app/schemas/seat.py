from datetime import datetime
from pydantic import BaseModel, Field


class SeatGenerateIn(BaseModel):
    event_id: int
    total_seats: int = Field(gt=0, le=5000)
    prefix: str = "S"   # S1..Sn


class SeatOut(BaseModel):
    id: int
    event_id: int
    seat_number: str
    status: str
    held_by_user_id: int | None = None
    hold_expires_at: datetime | None = None

    class Config:
        from_attributes = True


class SeatHoldIn(BaseModel):
    event_id: int
    seat_numbers: list[str] = Field(min_length=1)


class SeatConfirmIn(BaseModel):
    event_id: int
    seat_numbers: list[str] = Field(min_length=1)


class SeatReleaseIn(BaseModel):
    event_id: int
    seat_numbers: list[str] = Field(min_length=1)