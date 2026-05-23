from typing import List
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import  CategoryResponse

class GetAllCategoriesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self) -> List[CategoryResponse]:
        with self._database.session() as session:
            categories = self._repo.get_all(session)
            
            result = []
            for category in categories:
                result.append(CategoryResponse.model_validate(obj=category))
            
            return result
