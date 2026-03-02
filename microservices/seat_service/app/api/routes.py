from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.jwt import require_roles, get_current_user_payload
from app.schemas.seat import SeatGenerateIn, SeatOut, SeatHoldIn, SeatConfirmIn, SeatReleaseIn
from app.services.seat_service import generate_seats, get_event_seats, hold_seats, confirm_seats, release_seats

router = APIRouter(prefix="/seats", tags=["Seats"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/generate", status_code=201)
def generate(payload: SeatGenerateIn, db: Session = Depends(get_db),
             _=Depends(require_roles("organizer", "admin"))):
    count = generate_seats(db, payload.event_id, payload.total_seats, payload.prefix)
    return {"created": count}


@router.get("/{event_id}", response_model=list[SeatOut])
def list_for_event(event_id: int, db: Session = Depends(get_db)):
    return get_event_seats(db, event_id)


@router.post("/hold", response_model=list[SeatOut])
def hold(payload: SeatHoldIn, db: Session = Depends(get_db), user=Depends(get_current_user_payload)):
    try:
        return hold_seats(db, event_id=payload.event_id, seat_numbers=payload.seat_numbers, user_id=int(user["sub"]))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/confirm", response_model=list[SeatOut])
def confirm(payload: SeatConfirmIn, db: Session = Depends(get_db), user=Depends(get_current_user_payload)):
    try:
        return confirm_seats(db, event_id=payload.event_id, seat_numbers=payload.seat_numbers, user_id=int(user["sub"]))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/release", response_model=list[SeatOut])
def release(payload: SeatReleaseIn, db: Session = Depends(get_db), user=Depends(get_current_user_payload)):
    try:
        return release_seats(db, event_id=payload.event_id, seat_numbers=payload.seat_numbers, user_id=int(user["sub"]))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))