from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.seat import Seat


def bulk_create_seats(db: Session, seats: list[Seat]) -> None:
    db.add_all(seats)
    db.commit()


def list_seats_for_event(db: Session, event_id: int) -> list[Seat]:
    stmt = select(Seat).where(Seat.event_id == event_id).order_by(Seat.seat_number.asc())
    return list(db.execute(stmt).scalars().all())


def get_seats_for_update(db: Session, event_id: int, seat_numbers: list[str]) -> list[Seat]:
    """
    Locks selected seats so two users can't book the same seat at same time.
    Works well in Postgres using SELECT ... FOR UPDATE.
    """
    stmt = (
        select(Seat)
        .where(Seat.event_id == event_id, Seat.seat_number.in_(seat_numbers))
        .with_for_update()
    )
    return list(db.execute(stmt).scalars().all())