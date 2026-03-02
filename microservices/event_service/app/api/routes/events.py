from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles, get_current_user
from app.schemas.event_schema import EventCreate, EventOut, EventStatusOut
from app.services.event_service import (
    create_event_draft,
    publish_event,
    cancel_event,
    list_public_events,
    list_all_events,
)

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("", response_model=EventOut, status_code=201)
def create_event(
    payload: EventCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("organizer", "admin")),
):
    try:
        return create_event_draft(db, organizer_id=user.id, payload=payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/published", response_model=list[EventOut])
def get_published_events(db: Session = Depends(get_db)):
    return list_public_events(db)


@router.get("", response_model=list[EventOut])
def get_all_events(
    status: str | None = None,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin")),  # only admin can view all
):
    try:
        return list_all_events(db, status=status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{event_id}/publish", response_model=EventStatusOut)
def publish(
    event_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("organizer", "admin")),
):
    try:
        return publish_event(db, event_id=event_id, organizer_id=user.id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{event_id}/cancel", response_model=EventStatusOut)
def cancel(
    event_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("organizer", "admin")),
):
    try:
        return cancel_event(db, event_id=event_id, organizer_id=user.id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))