from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.seat import Seat


def bulk_create_seats(db: Session, event_id: int, seat_numbers: list[str]) -> int:
    db.add_all([Seat(event_id=event_id, seat_number=s, status="available") for s in seat_numbers])
    db.commit()
    return len(seat_numbers)


def list_seats_by_event(db: Session, event_id: int) -> list[Seat]:
    stmt = select(Seat).where(Seat.event_id == event_id).order_by(Seat.seat_number.asc())
    return list(db.execute(stmt).scalars().all())


def get_seats_for_update(db: Session, event_id: int, seat_numbers: list[str]) -> list[Seat]:
    # row lock to avoid race
    stmt = (
        select(Seat)
        .where(Seat.event_id == event_id, Seat.seat_number.in_(seat_numbers))
        .with_for_update()
    )
    return list(db.execute(stmt).scalars().all())