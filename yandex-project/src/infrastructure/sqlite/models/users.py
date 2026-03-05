from infrastructure.sqlite.database import Base

from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import String



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        unique=True
    )
    login: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )
    email: Mapped[str] = mapped_column(
        nullable=False
    )
    password: Mapped[str] = mapped_column(
        nullable=False
    )
    first_name: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    second_name: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
