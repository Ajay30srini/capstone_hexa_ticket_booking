from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles
from app.schemas.booking_schema import BookingCreate, BookingOut
from app.services.booking_service import create_booking_confirmed

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("", response_model=BookingOut, status_code=201)
def create_booking(
    payload: BookingCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("customer", "admin", "organizer")),
):
    try:
        booking = create_booking_confirmed(
            db=db,
            user_id=user.id,
            event_id=payload.event_id,
            seat_numbers=payload.seat_numbers,
        )
        return BookingOut(
            id=booking.id,
            user_id=booking.user_id,
            event_id=booking.event_id,
            status=booking.status,
            created_at=booking.created_at,
            seat_numbers=booking.seat_numbers_csv.split(","),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))