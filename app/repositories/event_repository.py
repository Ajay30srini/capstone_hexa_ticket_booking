from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.event import Event


def create_event(db: Session, event: Event) -> Event:
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def list_events(db: Session) -> list[Event]:
    stmt = select(Event).order_by(Event.date.asc())
    return list(db.execute(stmt).scalars().all())


def get_event(db: Session, event_id: int) -> Event | None:
    stmt = select(Event).where(Event.id == event_id)
    return db.execute(stmt).scalars().first()