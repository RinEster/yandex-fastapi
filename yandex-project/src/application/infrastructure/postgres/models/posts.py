from infrastructure.sqlite.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy import String, Text, DateTime, Boolean, ForeignKey

from datetime import datetime

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        unique=True
    )
    title: Mapped[str] = mapped_column(
        String(256),
        nullable=False
    )
    text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    pub_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id"),
        nullable=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True
    )
    image: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )
    is_published: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

    author = relationship("User", back_populates="posts")
    location = relationship("Location", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
