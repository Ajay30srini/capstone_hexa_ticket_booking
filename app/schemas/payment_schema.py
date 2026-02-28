from pydantic import BaseModel, Field


class PaymentConfirmIn(BaseModel):
    booking_id: int
    payment_reference: str = Field(min_length=3, max_length=100)


class PaymentConfirmOut(BaseModel):
    booking_id: int
    status: str
    message: str