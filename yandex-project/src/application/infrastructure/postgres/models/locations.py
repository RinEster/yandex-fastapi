from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from ..database import Base


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, unique=True
    )
    name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    is_published: Mapped[bool] = mapped_column(
        Boolean, default=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    posts = relationship("Post", back_populates="location")
