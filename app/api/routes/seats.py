from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.seat_schema import SeatListOut, SeatOut
from app.services.seat_service import get_event_seats

router = APIRouter(prefix="/events", tags=["Seats"])


@router.get("/{event_id}/seats", response_model=SeatListOut)
def list_event_seats(event_id: int, db: Session = Depends(get_db)):
    try:
        data = get_event_seats(db, event_id)
        return SeatListOut(
            event_id=data["event_id"],
            total=data["total"],
            available=data["available"],
            booked=data["booked"],
            seats=[SeatOut.model_validate(s) for s in data["seats"]],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))