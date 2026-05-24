from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class LocationBase(BaseModel):
    name: str = Field(
        ...,
        max_length=256,
        description="Название места",
    )
    is_published: bool = Field(
        True, description="Опубликовано"
    )


class LocationResponse(LocationBase):
    id: int
    created_at: datetime = Field(
        ..., description="Добавлено"
    )
    model_config = ConfigDict(
        from_attributes=True
    )


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: str | None = Field(
        None,
        max_length=256,
        description="Название места",
    )
    is_published: bool | None = Field(
        None, description="Опубликовано"
    )
