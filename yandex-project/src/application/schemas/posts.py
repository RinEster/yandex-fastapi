from datetime import UTC, datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


from typing import List

class PostImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    image_url: str

class PostBase(BaseModel):
    title: str = Field(
        ...,
        max_length=256,
        description="Заголовок",
    )
    text: str = Field(..., description="Текст")
    pub_date: datetime = Field(
        ..., description="Дата и время публикации"
    )
    location_id: int | None = Field(
        None, description="Местоположение"
    )
    category_id: int | None = Field(
        None, description="Категория"
    )
    is_published: bool = Field(
        True, description="Опубликовано"
    )

    @field_validator("pub_date")
    @classmethod
    def normalize_pub_date(
        cls, value: datetime
    ) -> datetime:
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value


class PostCreate(PostBase):
    images: List[PostImageResponse] = Field(
        default_factory=list,
        description="Список объектов изображений с id"
    )


class PostUpdate(BaseModel):
    title: str | None = Field(
        None, max_length=256
    )
    text: str | None = None
    pub_date: datetime | None = None
    location_id: int | None = None
    category_id: int | None = None
    images: List[str] | None = Field(
        None,
        description="Новый список путей к изображениям"
    )
    is_published: bool | None = None

    @field_validator("pub_date")
    @classmethod
    def normalize_pub_date(
        cls, value: datetime | None
    ) -> datetime | None:
        if value is None:
            return value

        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)

        return value


class PostResponse(PostBase):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: int
    author_id: int
    created_at: datetime
    images: List[PostImageResponse] = Field(
        default_factory=list,
        description="Список объектов изображений с id"
    )
