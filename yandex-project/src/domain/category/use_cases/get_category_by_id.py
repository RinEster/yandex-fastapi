from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import Category as CategorySchema

class GetCategoryByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> CategorySchema:
        with self._database.session() as session:
            category = self._repo.get_by_id(session, category_id)
            
            if not category:
                raise ValueError("Категория не найдена")
            
            category_dict = {
                "id": category.id,
                "title": category.title,
                "description": category.description,
                "slug": category.slug,
                "is_published": category.is_published,
                "created_at": category.created_at
            }
            
            return CategorySchema.model_validate(obj=category_dict)
