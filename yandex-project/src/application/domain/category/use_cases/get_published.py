from typing import List

from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.categories import (
    CategoryRepository,
)
from application.schemas.categories import CategoryResponse


class GetPublishedCategoriesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self) -> List[CategoryResponse]:
        async with self._database.session() as session:
            categories = await self._repo.get_published(session)

            return [
                CategoryResponse.model_validate(obj=category)
                for category in categories
            ]
