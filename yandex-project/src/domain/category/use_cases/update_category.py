from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import Category as CategorySchema

class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self,
        category_id: int,
        title: str,
        description: str,
        slug: str,
        is_published: bool = True
    ) -> CategorySchema:
        with self._database.session() as session:
            category = self._repo.get_by_id(session, category_id)
            if not category:
                raise ValueError("Категория не найдена")
            
            updated = self._repo.update(
                session,
                category_id,
                title,
                description,
                slug,
                is_published
            )
            session.commit()
            
            category_dict = {
                "id": updated.id,
                "title": updated.title,
                "description": updated.description,
                "slug": updated.slug,
                "is_published": updated.is_published,
                "created_at": updated.created_at
            }
            
            return CategorySchema.model_validate(obj=category_dict)
