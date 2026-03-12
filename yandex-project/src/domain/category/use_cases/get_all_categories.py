from typing import List
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import Category as CategorySchema

class GetAllCategoriesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self) -> List[CategorySchema]:
        with self._database.session() as session:
            categories = self._repo.get_all(session)
            
            result = []
            for category in categories:
                category_dict = {
                    "id": category.id,
                    "title": category.title,
                    "description": category.description,
                    "slug": category.slug,
                    "is_published": category.is_published,
                    "created_at": category.created_at
                }
                result.append(CategorySchema.model_validate(obj=category_dict))
            
            return result
