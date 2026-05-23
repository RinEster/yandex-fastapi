from pydantic import BaseModel, Field

from schemas.users import User 
from schemas.categories import Category
from schemas.locations import Location
from datetime import datetime

class Post(BaseModel):
    id: int
    title: str = Field(..., max_length=256, description='Заголовок')
    text: str = Field(..., description='Текст')
    pub_date: datetime = Field(..., description='Дата и время публикации')
    author_id: int = Field(...,description='Автор публикации')
    location_id: int | None = Field(None,description='Местоположение')
    category_id: int | None = Field(None,description='Категория')
    image: str | None = Field(None, description="Путь к изображению")
    is_published: bool = Field(True,description='Опубликовано')
    created_at: datetime = Field(...,description='Добавлено')


class Comment(BaseModel):
    id: int
    post_id: int = Field(...,description='Публикация')
    author_id: int = Field(...,description='Автор комментария')
    text: str = Field(...,description='Текст комментария')
    created_at: datetime = Field(...,description='Добавлено')
