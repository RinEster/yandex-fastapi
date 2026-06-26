from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from typing import List

from ..database import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, unique=True
    )
    title: Mapped[str] = mapped_column(
        String(256), nullable=False
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    pub_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    location_id: Mapped[int | None] = mapped_column(
        ForeignKey("locations.id"), nullable=True
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"), nullable=True
    )
    is_published: Mapped[bool] = mapped_column(
        Boolean, default=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    author = relationship("User", back_populates="posts")
    location = relationship(
        "Location", back_populates="posts"
    )
    category = relationship(
        "Category", back_populates="posts"
    )
    comments = relationship(
        "Comment", back_populates="post"
    )
    images: Mapped[List["PostImage"]] = relationship(back_populates="post", cascade="all, delete-orphan")


class PostImage(Base):
    __tablename__ = "post_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    post = relationship("Post",back_populates="images")
