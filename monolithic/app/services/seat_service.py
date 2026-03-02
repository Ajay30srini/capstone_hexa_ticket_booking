from sqlalchemy.orm import Session

from app.repositories.event_repository import get_event
from app.repositories.seat_repository import list_seats_for_event


def get_event_seats(db: Session, event_id: int):
    event = get_event(db, event_id)
    if not event:
        raise ValueError("Event not found")

    seats = list_seats_for_event(db, event_id)
    available = sum(1 for s in seats if s.status == "available")
    booked = sum(1 for s in seats if s.status == "booked")

    return {
        "event_id": event_id,
        "total": len(seats),
        "available": available,
        "booked": booked,
        "seats": seats,
    }