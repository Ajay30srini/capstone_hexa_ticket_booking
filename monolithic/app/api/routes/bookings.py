from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles
from app.schemas.booking_schema import BookingCreate, BookingOut, BookingCancelOut
from app.services.booking_service import create_booking_hold, cancel_booking, expire_booking_admin
from app.repositories.booking_repository import list_bookings_for_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("", response_model=BookingOut, status_code=201)
def create_booking(
    payload: BookingCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("customer", "admin", "organizer")),
):
    """
    Sprint 4: This creates a HOLD (pending booking) and marks seats as HELD.
    Confirm it using POST /payments/confirm
    """
    try:
        booking = create_booking_hold(
            db=db,
            user_id=user.id,
            requester_role=user.role,
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
    out: list[BookingOut] = []
    for b in bookings:
        out.append(
            BookingOut(
                id=b.id,
                user_id=b.user_id,
                event_id=b.event_id,
                status=b.status,
                created_at=b.created_at,
                seat_numbers=b.seat_numbers_csv.split(",") if b.seat_numbers_csv else [],
            )
        )
    return out


@router.patch("/{booking_id}/cancel", response_model=BookingCancelOut)
def cancel(
    booking_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("customer", "admin", "organizer")),
):
    try:
        b = cancel_booking(db, booking_id, requester_id=user.id, requester_role=user.role)
        return BookingCancelOut(
            id=b.id,
            status=b.status,
            event_id=b.event_id,
            user_id=b.user_id,
            seat_numbers=b.seat_numbers_csv.split(",") if b.seat_numbers_csv else [],
            cancelled_at=None,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{booking_id}/expire", response_model=BookingCancelOut)
def expire(
    booking_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_roles("admin")),
):
    try:
        b = expire_booking_admin(db, booking_id)
        return BookingCancelOut(
            id=b.id,
            status=b.status,
            event_id=b.event_id,
            user_id=b.user_id,
            seat_numbers=b.seat_numbers_csv.split(",") if b.seat_numbers_csv else [],
            cancelled_at=None,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))