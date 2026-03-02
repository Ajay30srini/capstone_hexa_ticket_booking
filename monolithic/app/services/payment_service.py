from sqlalchemy.orm import Session

from app.services.booking_service import confirm_booking_after_payment


def confirm_payment(db: Session, booking_id: int, payment_reference: str):
    # Mock: accept any non-empty reference as "paid"
    if not payment_reference or not payment_reference.strip():
        raise ValueError("Invalid payment reference")

    booking = confirm_booking_after_payment(db, booking_id)
    return booking