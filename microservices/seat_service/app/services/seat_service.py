from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.seat import Seat
from app.repos.seat_repo import bulk_create_seats, list_seats_by_event, get_seats_for_update

HOLD_MINUTES = 5


def generate_seats(db: Session, event_id: int, total_seats: int, prefix: str = "S") -> int:
    seat_numbers = [f"{prefix}{i}" for i in range(1, total_seats + 1)]
    return bulk_create_seats(db, event_id, seat_numbers)


def get_event_seats(db: Session, event_id: int) -> list[Seat]:
    return list_seats_by_event(db, event_id)


def hold_seats(db: Session, *, event_id: int, seat_numbers: list[str], user_id: int) -> list[Seat]:
    seats = get_seats_for_update(db, event_id, seat_numbers)
    if len(seats) != len(seat_numbers):
        raise ValueError("One or more seats not found")

    now = datetime.utcnow()
    expires = now + timedelta(minutes=HOLD_MINUTES)

    for s in seats:
        if s.status == "booked":
            raise ValueError(f"Seat already booked: {s.seat_number}")

        # if held but expired -> release automatically
        if s.status == "held" and s.hold_expires_at and s.hold_expires_at < now:
            s.status = "available"
            s.held_by_user_id = None
            s.hold_expires_at = None

        if s.status != "available":
            raise ValueError(f"Seat not available: {s.seat_number}")

    for s in seats:
        s.status = "held"
        s.held_by_user_id = user_id
        s.hold_expires_at = expires

    db.commit()
    for s in seats:
        db.refresh(s)
    return seats


def confirm_seats(db: Session, *, event_id: int, seat_numbers: list[str], user_id: int) -> list[Seat]:
    seats = get_seats_for_update(db, event_id, seat_numbers)
    if len(seats) != len(seat_numbers):
        raise ValueError("One or more seats not found")

    now = datetime.utcnow()
    for s in seats:
        if s.status == "booked":
            raise ValueError(f"Seat already booked: {s.seat_number}")
        if s.status != "held":
            raise ValueError(f"Seat not held: {s.seat_number}")
        if s.held_by_user_id != user_id:
            raise ValueError(f"Seat held by another user: {s.seat_number}")
        if s.hold_expires_at and s.hold_expires_at < now:
            raise ValueError(f"Seat hold expired: {s.seat_number}")

    for s in seats:
        s.status = "booked"
        s.hold_expires_at = None

    db.commit()
    for s in seats:
        db.refresh(s)
    return seats


def release_seats(db: Session, *, event_id: int, seat_numbers: list[str], user_id: int) -> list[Seat]:
    seats = get_seats_for_update(db, event_id, seat_numbers)
    if len(seats) != len(seat_numbers):
        raise ValueError("One or more seats not found")

    for s in seats:
        if s.status == "held" and s.held_by_user_id == user_id:
            s.status = "available"
            s.held_by_user_id = None
            s.hold_expires_at = None

    db.commit()
    for s in seats:
        db.refresh(s)
    return seats