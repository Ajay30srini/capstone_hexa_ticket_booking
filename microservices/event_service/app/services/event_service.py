from sqlalchemy.orm import Session

from app.repositories.event_repository import (
    create_event,
    get_event_by_id,
    list_events,
    update_event_status,
)

VALID_STATUS = {"draft", "published", "cancelled"}


def create_event_draft(db: Session, *, organizer_id: int, payload):
    # payload is EventCreate (pydantic)
    return create_event(
        db,
        title=payload.title,
        description=payload.description,
        venue=payload.venue,
        event_date=payload.event_date,
        total_seats=payload.total_seats,
        organizer_id=organizer_id,
    )


def publish_event(db: Session, *, event_id: int, organizer_id: int):
    event = get_event_by_id(db, event_id)
    if not event:
        raise ValueError("Event not found")

    if event.organizer_id != organizer_id:
        raise PermissionError("Not your event")

    if event.status == "cancelled":
        raise ValueError("Cancelled event cannot be published")

    return update_event_status(db, event, "published")


def cancel_event(db: Session, *, event_id: int, organizer_id: int):
    event = get_event_by_id(db, event_id)
    if not event:
        raise ValueError("Event not found")

    if event.organizer_id != organizer_id:
        raise PermissionError("Not your event")

    if event.status == "cancelled":
        return event

    return update_event_status(db, event, "cancelled")


def list_public_events(db: Session):
    return list_events(db, status="published")


def list_all_events(db: Session, status: str | None = None):
    if status and status not in VALID_STATUS:
        raise ValueError("Invalid status filter")
    return list_events(db, status=status)