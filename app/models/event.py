from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    venue: Mapped[str] = mapped_column(String(200), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    total_seats: Mapped[int] = mapped_column(Integer, nullable=False)

    organizer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    # relationships
    seats = relationship("Seat", back_populates="event", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="event", cascade="all, delete-orphan")