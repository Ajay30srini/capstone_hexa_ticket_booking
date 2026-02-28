from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.repositories.booking_repository import get_booking
from app.repositories.event_repository import get_event
from app.repositories.seat_repository import get_seats_for_update


def create_booking_confirmed(
    db: Session,
    user_id: int,
    event_id: int,
    seat_numbers: list[str],
) -> Booking:
    event = get_event(db, event_id)
    if not event:
        raise ValueError("Event not found")

    seat_numbers = [s.strip().upper() for s in seat_numbers if s and s.strip()]
    if not seat_numbers:
        raise ValueError("No valid seats provided")

    seats = get_seats_for_update(db, event_id, seat_numbers)

    if len(seats) != len(set(seat_numbers)):
        raise ValueError("One or more seats do not exist")

    not_available = [s.seat_number for s in seats if s.status != "available"]
    if not_available:
        raise ValueError(f"Seats not available: {', '.join(not_available)}")

    for s in seats:
        s.status = "booked"

    booking = Booking(
        user_id=user_id,
        event_id=event_id,
        status="confirmed",
        created_at=datetime.now(timezone.utc),
        seat_numbers_csv=",".join(seat_numbers),
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def cancel_booking(
    db: Session,
    booking_id: int,
    requester_id: int,
    requester_role: str,
) -> Booking:
    booking = get_booking(db, booking_id)
    if not booking:
        raise ValueError("Booking not found")

    if requester_role != "admin" and booking.user_id != requester_id:
        raise ValueError("You are not allowed to cancel this booking")

    if booking.status == "cancelled":
        raise ValueError("Booking already cancelled")

    seat_numbers = [s.strip().upper() for s in booking.seat_numbers_csv.split(",") if s.strip()]
    if not seat_numbers:
        raise ValueError("No seats found in this booking")

    seats = get_seats_for_update(db, booking.event_id, seat_numbers)
    for s in seats:
        s.status = "available"

    booking.status = "cancelled"

    db.commit()
    db.refresh(booking)
    return booking