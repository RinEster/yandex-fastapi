from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategoryResponse, CategoryCreate, Category
from fastapi import HTTPException, status
from core.exceptions.database_exceptions import(
    CategoryTitleAlreadyExistsException,
    CategorySlugAlreadyExistsException
)
from core.exceptions.domain_exception import(
    CategorySlugIsNotUniqueException,
    CategoryTitleIsNotUniqueException
)
import logging

logger = logging.getLogger(__name__)

class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self, 
        data: CategoryCreate
    ) -> CategoryResponse:
        with self._database.session() as session:
            try:
                category = self._repo.create(session=session,data=data)
            except CategoryTitleAlreadyExistsException:
                error = CategoryTitleIsNotUniqueException(title=data.title)
                logger.error(error.get_detail())
                raise error
            except CategorySlugAlreadyExistsException:
                error = CategorySlugIsNotUniqueException(slug=data.slug)
                logger.error(error.get_detail())
                raise error
            return CategoryResponse.model_validate(obj=category)
