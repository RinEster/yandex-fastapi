from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class Category(BaseModel):
    title:str = Field(...,max_length=256, description='Заголовок')
    description: str = Field(..., description='Описание')
    slug: str = Field(..., description='Идентификатор страницы для URL')
    is_published: bool = Field(True, description='Опубликовано')
    created_at: datetime | None = Field(None, description='Добавлено')

class CategoryResponse(Category):
    id: int
    model_config = ConfigDict(from_attributes=True)

class CategoryCreate(Category):
    pass

class CategoryUpdate(BaseModel):
    title:str | None = Field(None, max_length=256, description='Заголовок')
    description: str | None = Field(None, description='Описание')
    slug: str | None = Field(None, description='Идентификатор страницы для URL')
    is_published: bool | None = Field(None, description='Опубликовано')

