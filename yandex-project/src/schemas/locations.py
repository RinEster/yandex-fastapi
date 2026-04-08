from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class Location(BaseModel):
    name: str = Field(..., max_length=256, description='Название места')
    is_published: bool = Field(True, description='Опубликовано')
    created_at: datetime = Field(..., description='Добавлено')

class LocationResponce(Location):
    id: int
    model_config = ConfigDict(from_attributes=True)

class LocationCreate(Location):
    pass

class LocationUpdate(BaseModel):
    name: str | None = Field(None, max_length=256, description='Название места')
    is_published: bool | None = Field(None, description='Опубликовано')
    created_at: datetime | None = Field(None, description='Добавлено')


