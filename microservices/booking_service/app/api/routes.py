from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.jwt import get_current_user_payload, get_token
from app.schemas.booking import BookingHoldIn, BookingOut
from app.services.booking_service import create_booking_hold, confirm_booking, cancel_booking
from app.repos.booking_repo import list_my_bookings

router = APIRouter(prefix="/bookings", tags=["Bookings"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/hold", response_model=BookingOut, status_code=201)
async def hold(payload: BookingHoldIn, db: Session = Depends(get_db),
               user=Depends(get_current_user_payload), token: str = Depends(get_token)):
    try:
        return await create_booking_hold(
            db,
            token=token,
            user_id=int(user["sub"]),
            event_id=payload.event_id,
            seat_numbers=payload.seat_numbers,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{booking_id}/confirm", response_model=BookingOut)
async def confirm(booking_id: int, db: Session = Depends(get_db),
                  user=Depends(get_current_user_payload), token: str = Depends(get_token)):
    try:
        return await confirm_booking(db, token=token, user_id=int(user["sub"]), booking_id=booking_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{booking_id}/cancel", response_model=BookingOut)
async def cancel(booking_id: int, db: Session = Depends(get_db),
                 user=Depends(get_current_user_payload), token: str = Depends(get_token)):
    try:
        return await cancel_booking(db, token=token, user_id=int(user["sub"]), booking_id=booking_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my", response_model=list[BookingOut])
def my(db: Session = Depends(get_db), user=Depends(get_current_user_payload)):
    return list_my_bookings(db, int(user["sub"]))