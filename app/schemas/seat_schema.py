from pydantic import BaseModel


class SeatOut(BaseModel):
    id: int
    event_id: int
    seat_number: str
    status: str

    class Config:
        from_attributes = True