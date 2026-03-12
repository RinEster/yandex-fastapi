from infrastructure.sqlite.database import Base

from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import String, Text, Boolean, DateTime

from datetime import datetime

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        unique=True
    )
    title: Mapped[str] = mapped_column(
        String(256),
        nullable=False
    )
    desctiption: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    slug: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    is_published: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime
    )

