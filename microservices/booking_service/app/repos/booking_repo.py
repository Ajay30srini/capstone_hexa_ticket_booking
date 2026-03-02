from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.booking import Booking

def create_booking(db: Session, *, user_id: int, event_id: int, seat_numbers: list[str]) -> Booking:
    b = Booking(user_id=user_id, event_id=event_id, seat_numbers=seat_numbers, status="pending")
    db.add(b)
    db.commit()
    db.refresh(b)
    return b

def get_booking(db: Session, booking_id: int) -> Booking | None:
    return db.execute(select(Booking).where(Booking.id == booking_id)).scalars().first()

def list_my_bookings(db: Session, user_id: int) -> list[Booking]:
    stmt = select(Booking).where(Booking.user_id == user_id).order_by(Booking.id.desc())
    return list(db.execute(stmt).scalars().all())

def save(db: Session, booking: Booking) -> Booking:
    db.commit()
    db.refresh(booking)
    return booking