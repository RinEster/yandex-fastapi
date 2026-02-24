from pydantic import BaseModel, Field
from datetime import datetime

class Category(BaseModel):
    title:str = Field(...,max_length=256, description='Заголовок')
    description: str = Field(..., description='Описание')
    slug: str = Field(..., description='Идентификатор страницы для URL')
    is_published: bool = Field(True, description='Опубликовано')
    created_at: datetime = Field(..., description='Добавлено')