from pydantic import BaseModel

class PaymentConfirmIn(BaseModel):
    booking_id: int
    success: bool = True