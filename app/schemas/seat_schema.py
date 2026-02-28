
from pydantic import BaseModel


class SeatOut(BaseModel):
    id: int
    event_id: int
    seat_number: str
    status: str

    class Config:
        from_attributes = True


class SeatListOut(BaseModel):
    event_id: int
    total: int
    available: int
    booked: int
    seats: list[SeatOut]