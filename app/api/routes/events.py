from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles
from app.schemas.event_schema import EventCreate, EventOut
from app.services.event_service import create_event_with_seats, get_all_events

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("", response_model=EventOut, status_code=201)
def create_event(
    payload: EventCreate,
    db: Session = Depends(get_db),
    organizer=Depends(require_roles("organizer", "admin")),
):
    try:
        event = create_event_with_seats(
            db=db,
            organizer_id=organizer.id,
            title=payload.title,
            venue=payload.venue,
            date=payload.date,
            total_seats=payload.total_seats,
        )
        return event
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[EventOut])
def list_events(db: Session = Depends(get_db)):
    return get_all_events(db)