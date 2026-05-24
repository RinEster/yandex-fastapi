from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from ..database import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, nullable=False
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id"), nullable=False
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
