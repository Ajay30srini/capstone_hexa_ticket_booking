from datetime import datetime
from sqlalchemy.orm import Session

from app.clients.event_client import ensure_event_is_published
from app.clients.seat_client import hold_seats, confirm_seats, release_seats
from app.models.booking import Booking
from app.repos.booking_repo import create_booking, get_booking, save

async def create_booking_hold(db: Session, *, token: str, user_id: int, event_id: int, seat_numbers: list[str]) -> Booking:
    await ensure_event_is_published(event_id)
    await hold_seats(token, event_id, seat_numbers)
    return create_booking(db, user_id=user_id, event_id=event_id, seat_numbers=seat_numbers)

async def confirm_booking(db: Session, *, token: str, user_id: int, booking_id: int) -> Booking:
    b = get_booking(db, booking_id)
    if not b:
        raise ValueError("Booking not found")
    if b.user_id != user_id:
        raise PermissionError("Not your booking")

    if b.status == "confirmed":
        return b
    if b.status == "cancelled":
        raise ValueError("Booking already cancelled")

    await confirm_seats(token, b.event_id, b.seat_numbers)

    b.status = "confirmed"
    b.confirmed_at = datetime.utcnow()
    return save(db, b)

async def cancel_booking(db: Session, *, token: str, user_id: int, booking_id: int) -> Booking:
    b = get_booking(db, booking_id)
    if not b:
        raise ValueError("Booking not found")
    if b.user_id != user_id:
        raise PermissionError("Not your booking")

    if b.status == "cancelled":
        return b
    if b.status == "confirmed":
        # you can decide refund policy later; we still release seats here for simplicity
        pass

    # best effort release
    try:
        await release_seats(token, b.event_id, b.seat_numbers)
    except Exception:
        pass

    b.status = "cancelled"
    b.cancelled_at = datetime.utcnow()
    return save(db, b)