from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, DateTime, ForeignKey
from datetime import datetime

class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        unique=True,
        nullable=False
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id"),
        nullable=False
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )
    
    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
