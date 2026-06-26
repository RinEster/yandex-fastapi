from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, Field

class CommentImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    image_url: str

class CommentImageCreate(BaseModel):
    image_url: str

class CommentBase(BaseModel):
    text: str = Field(
        ..., description="Текст комментария"
    )

class CommentCreate(CommentBase):
    post_id: int = Field(
        ..., description="ID публикации"
    )
    images: List[CommentImageCreate] = Field(
        default_factory=list,
        description="Список путей к изображениям (без ID)"
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
    images: List[CommentImageResponse] = Field(
        default_factory=list,
        description="Список объектов изображений с ID"
    )
    
    model_config = ConfigDict(
        from_attributes=True
    )
