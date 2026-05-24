from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    title: str = Field(
        ...,
        max_length=256,
        description="Заголовок",
    )
    description: str = Field(..., description="Описание")
    slug: str = Field(
        ...,
        max_length=100,
        pattern=r"^[a-z0-9_-]+$",
        description="Идентификатор страницы для URL",
    )
    is_published: bool = Field(
        True, description="Опубликовано"
    )


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    title: str | None = Field(
        None,
        max_length=256,
        description="Заголовок",
    )
    description: str | None = Field(
        None, description="Описание"
    )
    slug: str | None = Field(
        None,
        max_length=100,
        pattern=r"^[a-z0-9_-]+$",
        description="Идентификатор страницы для URL",
    )
    is_published: bool | None = Field(
        None, description="Опубликовано"
    )


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime = Field(
        ..., description="Добавлено"
    )

    model_config = ConfigDict(from_attributes=True)
