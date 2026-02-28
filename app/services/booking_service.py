from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.constants import (
    HOLD_MINUTES,
    SEAT_STATUS_AVAILABLE,
    SEAT_STATUS_HELD,
    SEAT_STATUS_BOOKED,
    BOOKING_PENDING,
    BOOKING_CONFIRMED,
    BOOKING_CANCELLED,
    BOOKING_EXPIRED,
)
from app.models.booking import Booking
from app.repositories.booking_repository import get_booking
from app.repositories.event_repository import get_event
from app.repositories.seat_repository import get_seats_for_update


def _normalize_seats(seat_numbers: list[str]) -> list[str]:
    seats = [s.strip().upper() for s in seat_numbers if s and s.strip()]
    return seats


def create_booking_hold(
    db: Session,
    user_id: int,
    requester_role: str,
    event_id: int,
    seat_numbers: list[str],
) -> Booking:
    event = get_event(db, event_id)
    if not event:
        raise ValueError("Event not found")

    if event.status != "published":
        raise ValueError("Bookings allowed only for published events")

    if requester_role == "organizer" and event.organizer_id == user_id:
        raise ValueError("Organizer cannot book their own event")

    seat_numbers = _normalize_seats(seat_numbers)
    if not seat_numbers:
        raise ValueError("No valid seats provided")

    # Lock seats
    seats = get_seats_for_update(db, event_id, seat_numbers)

    if len(seats) != len(set(seat_numbers)):
        raise ValueError("One or more seats do not exist")

    not_available = [s.seat_number for s in seats if s.status != SEAT_STATUS_AVAILABLE]
    if not_available:
        raise ValueError(f"Seats not available: {', '.join(not_available)}")

    for s in seats:
        s.status = SEAT_STATUS_HELD

    now = datetime.now(timezone.utc)
    booking = Booking(
        user_id=user_id,
        event_id=event_id,
        status=BOOKING_PENDING,
        created_at=now,
        hold_expires_at=now + timedelta(minutes=HOLD_MINUTES),
        seat_numbers_csv=",".join(seat_numbers),
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def confirm_booking_after_payment(db: Session, booking_id: int) -> Booking:
    booking = get_booking(db, booking_id)
    if not booking:
        raise ValueError("Booking not found")

    if booking.status != BOOKING_PENDING:
        raise ValueError(f"Booking is not pending (current: {booking.status})")

    now = datetime.now(timezone.utc)
    if booking.hold_expires_at and booking.hold_expires_at < now:
        # Expired hold -> mark expired + release seats
        _expire_booking(db, booking)
        raise ValueError("Hold expired. Please book again.")

    seat_numbers = _normalize_seats(booking.seat_numbers_csv.split(","))
    seats = get_seats_for_update(db, booking.event_id, seat_numbers)

    # Ensure they are still held
    bad = [s.seat_number for s in seats if s.status != SEAT_STATUS_HELD]
    if bad:
        raise ValueError(f"Seats not in held state: {', '.join(bad)}")

    for s in seats:
        s.status = SEAT_STATUS_BOOKED

    booking.status = BOOKING_CONFIRMED
    db.commit()
    db.refresh(booking)
    return booking


def cancel_booking(db: Session, booking_id: int, requester_id: int, requester_role: str) -> Booking:
    booking = get_booking(db, booking_id)
    if not booking:
        raise ValueError("Booking not found")

    if requester_role != "admin" and booking.user_id != requester_id:
        raise ValueError("You are not allowed to cancel this booking")

    if booking.status == BOOKING_CANCELLED:
        raise ValueError("Booking already cancelled")

    seat_numbers = _normalize_seats(booking.seat_numbers_csv.split(","))
    seats = get_seats_for_update(db, booking.event_id, seat_numbers)

    # If pending -> held seats should be released
    # If confirmed -> booked seats should be released
    for s in seats:
        s.status = SEAT_STATUS_AVAILABLE

    booking.status = BOOKING_CANCELLED

    db.commit()
    db.refresh(booking)
    return booking


def expire_booking_admin(db: Session, booking_id: int) -> Booking:
    booking = get_booking(db, booking_id)
    if not booking:
        raise ValueError("Booking not found")

    if booking.status != BOOKING_PENDING:
        raise ValueError(f"Only pending bookings can be expired (current: {booking.status})")

    now = datetime.now(timezone.utc)
    if booking.hold_expires_at and booking.hold_expires_at > now:
        raise ValueError("Hold not expired yet")

    _expire_booking(db, booking)
    return booking


def _expire_booking(db: Session, booking: Booking) -> None:
    seat_numbers = _normalize_seats(booking.seat_numbers_csv.split(","))
    seats = get_seats_for_update(db, booking.event_id, seat_numbers)
    for s in seats:
        if s.status == SEAT_STATUS_HELD:
            s.status = SEAT_STATUS_AVAILABLE
    booking.status = BOOKING_EXPIRED
    db.commit()
    db.refresh(booking)