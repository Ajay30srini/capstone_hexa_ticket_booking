from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.booking import Booking
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

    seat_numbers = [s.strip().upper() for s in seat_numbers if s.strip()]
    if not seat_numbers:
        raise ValueError("No valid seats provided")

    seats = get_seats_for_update(db, event_id, seat_numbers)

    if len(seats) != len(set(seat_numbers)):
        raise ValueError("One or more seats do not exist")

    not_available = [s.seat_number for s in seats if s.status != "available"]
    if not_available:
        raise ValueError(f"Seats not available: {', '.join(not_available)}")

    # Mark seats booked
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