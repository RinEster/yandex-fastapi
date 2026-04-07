from typing import List
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategoryResponse

class GetPublishedCategoriesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self) -> List[CategoryResponse]:
        with self._database.session() as session:
            categories = self._repo.get_published(session)
            
            return [
                CategoryResponse.model_validate(obj=category) 
                for category in categories
            ]
