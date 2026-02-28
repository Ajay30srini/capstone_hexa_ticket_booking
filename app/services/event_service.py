from sqlalchemy.orm import Session

from app.models.event import Event
from app.models.seat import Seat
from app.repositories.event_repository import create_event, list_events_published
from app.repositories.seat_repository import bulk_create_seats


def create_event_with_seats(
    db: Session,
    organizer_id: int,
    title: str,
    venue: str,
    date,
    total_seats: int,
) -> Event:
    event = Event(
        title=title,
        venue=venue,
        date=date,
        total_seats=total_seats,
        organizer_id=organizer_id,
        status="draft",
    )

    event = create_event(db, event)

    seats = [Seat(event_id=event.id, seat_number=f"S{i}", status="available") for i in range(1, total_seats + 1)]
    bulk_create_seats(db, seats)

    return event


def get_all_events(db: Session):
    return list_events_published(db)