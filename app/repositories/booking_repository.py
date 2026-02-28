from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.booking import Booking


def create_booking(db: Session, booking: Booking) -> Booking:
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def list_bookings_for_user(db: Session, user_id: int) -> list[Booking]:
    stmt = select(Booking).where(Booking.user_id == user_id).order_by(Booking.created_at.desc())
    return list(db.execute(stmt).scalars().all())


def get_booking(db: Session, booking_id: int) -> Booking | None:
    stmt = select(Booking).where(Booking.id == booking_id)
    return db.execute(stmt).scalars().first()