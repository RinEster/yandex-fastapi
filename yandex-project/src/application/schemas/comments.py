from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentBase(BaseModel):
    text: str = Field(
        ..., description="Текст комментария"
    )


class CommentCreate(CommentBase):
    post_id: int = Field(
        ..., description="ID публикации"
    )


class CommentUpdate(BaseModel):
    text: str | None = Field(
        None, description="Текст комментария"
    )


class CommentResponse(CommentBase):
    id: int
    post_id: int = Field(
        ..., description="ID публикации"
    )
    author_id: int = Field(
        ..., description="ID автора комментария"
    )
    created_at: datetime = Field(
        ..., description="Дата и время добавления"
    )

    model_config = ConfigDict(
        from_attributes=True
    )
