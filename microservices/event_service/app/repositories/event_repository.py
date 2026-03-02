from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.event import Event


def create_event(db: Session, *, title: str, description: str | None, venue: str | None,
                 event_date, total_seats: int, organizer_id: int) -> Event:
    event = Event(
        title=title,
        description=description,
        venue=venue,
        event_date=event_date,
        total_seats=total_seats,
        organizer_id=organizer_id,
        status="draft",
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_event_by_id(db: Session, event_id: int) -> Event | None:
    return db.execute(select(Event).where(Event.id == event_id)).scalars().first()


def list_events(db: Session, *, status: str | None = None) -> list[Event]:
    stmt = select(Event)
    if status:
        stmt = stmt.where(Event.status == status)
    stmt = stmt.order_by(Event.id.desc())
    return list(db.execute(stmt).scalars().all())


def update_event_status(db: Session, event: Event, new_status: str) -> Event:
    event.status = new_status
    db.commit()
    db.refresh(event)
    return event