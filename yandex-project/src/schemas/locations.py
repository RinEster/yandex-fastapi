from pydantic import BaseModel, Field
from datetime import datetime

class Location(BaseModel):
    id: int
    name: str = Field(..., max_length=256, description='Название места')
    is_published: bool = Field(True, description='Опубликовано')
    created_at: datetime = Field(..., description='Добавлено')
