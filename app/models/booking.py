from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False, index=True)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="confirmed")  # confirmed/cancelled
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # store seat list as comma-separated for sprint 2 simplicity
    seat_numbers_csv: Mapped[str] = mapped_column(String(500), nullable=False)

    event = relationship("Event", back_populates="bookings")