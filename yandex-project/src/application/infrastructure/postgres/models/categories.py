from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from ..database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, unique=True
    )
    title: Mapped[str] = mapped_column(
        String(256), unique=True, nullable=False
    )
    description: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    slug: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True
    )
    is_published: Mapped[bool] = mapped_column(
        Boolean, default=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    posts = relationship("Post", back_populates="category")
