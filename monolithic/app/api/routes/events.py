from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles
from app.schemas.event_schema import EventCreate, EventOut, EventStatusUpdate
from app.services.event_service import create_event_with_seats
from app.repositories.event_repository import (
    get_event,
    list_events_published,
    list_events_all,
    update_event_status,
)

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("", response_model=EventOut, status_code=201)
def create_event(
    payload: EventCreate,
    db: Session = Depends(get_db),
    organizer=Depends(require_roles("organizer", "admin")),
):
    event = create_event_with_seats(
        db=db,
        organizer_id=organizer.id,
        title=payload.title,
        venue=payload.venue,
        date=payload.date,
        total_seats=payload.total_seats,
    )
    return event


@router.get("", response_model=list[EventOut])
def list_events(db: Session = Depends(get_db)):
    # Public: only published
    return list_events_published(db)


@router.get("/all", response_model=list[EventOut])
def list_all_events(
    db: Session = Depends(get_db),
    user=Depends(require_roles("organizer", "admin")),
):
    # Organizer/Admin view: all events
    return list_events_all(db)


@router.patch("/{event_id}/status", response_model=EventOut)
def change_status(
    event_id: int,
    payload: EventStatusUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("organizer", "admin")),
):
    event = get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Only owner organizer can update, admin can update all
    if user.role != "admin" and event.organizer_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return update_event_status(db, event, payload.status)