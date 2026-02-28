from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles
from app.schemas.booking_schema import BookingCreate, BookingOut, BookingCancelOut
from app.services.booking_service import create_booking_confirmed, cancel_booking
from app.repositories.booking_repository import list_bookings_for_user

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


@router.get("/my", response_model=list[BookingOut])
def my_bookings(
    db: Session = Depends(get_db),
    user=Depends(require_roles("customer", "admin", "organizer")),
):
    bookings = list_bookings_for_user(db, user.id)
    return [
        BookingOut(
            id=b.id,
            user_id=b.user_id,
            event_id=b.event_id,
            status=b.status,
            created_at=b.created_at,
            seat_numbers=b.seat_numbers_csv.split(","),
        )
        for b in bookings
    ]


@router.patch("/{booking_id}/cancel", response_model=BookingCancelOut)
def cancel_my_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("customer", "admin", "organizer")),
):
    try:
        booking = cancel_booking(
            db=db,
            booking_id=booking_id,
            requester_id=user.id,
            requester_role=user.role,
        )
        return BookingCancelOut(
            id=booking.id,
            status=booking.status,
            event_id=booking.event_id,
            user_id=booking.user_id,
            seat_numbers=booking.seat_numbers_csv.split(","),
            cancelled_at=None,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))