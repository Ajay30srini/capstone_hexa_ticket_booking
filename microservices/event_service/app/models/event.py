from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    organizer_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    venue: Mapped[str | None] = mapped_column(String(200), nullable=True)
    event_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)

    total_seats: Mapped[int] = mapped_column(Integer, nullable=False)

    # sprint-3 status: draft/published/cancelled
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="draft")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=datetime.utcnow, nullable=False)