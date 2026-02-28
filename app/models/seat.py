from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Seat(Base):
    __tablename__ = "seats"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False, index=True)

    # like "A1", "A2" etc (we’ll generate as S1..Sn for now)
    seat_number: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="available")  # available|booked

    event = relationship("Event", back_populates="seats")

    __table_args__ = (
        UniqueConstraint("event_id", "seat_number", name="uq_event_seat_number"),
    )