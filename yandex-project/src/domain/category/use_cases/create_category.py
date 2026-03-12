from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import Category as CategorySchema

class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self, 
        title: str,
        description: str,
        slug: str,
        is_published: bool = True
    ) -> CategorySchema:
        with self._database.session() as session: 
            category = self._repo.create(
                session=session,
                title=title,
                description=description,
                slug=slug,
                is_published=is_published
            )
            session.commit()
            
            category_dict = {
                "id": category.id,
                "title": category.title,
                "description": category.description,
                "slug": category.slug,
                "is_published": category.is_published,
                "created_at": category.created_at
            }
            
            return CategorySchema.model_validate(obj=category_dict)
