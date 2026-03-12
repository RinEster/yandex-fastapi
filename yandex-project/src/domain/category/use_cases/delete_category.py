from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository

class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> bool:
        with self._database.session() as session:
            category = self._repo.get_by_id(session, category_id)
            if not category:
                raise ValueError("Категория не найдена")
            
            result = self._repo.delete(session, category_id)
            return result
