from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategoryResponse, CategoryUpdate
from core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    CategoryTitleAlreadyExistsException,
    CategorySlugAlreadyExistsException
)
from core.exceptions.domain_exception import (
    CategoryNotFoundByIdException,
    CategoryTitleIsNotUniqueException,
    CategorySlugIsNotUniqueException
)
import logging

logger = logging.getLogger(__name__)

class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self,
        category_id: int,
        data: CategoryUpdate
    ) -> CategoryResponse:
        with self._database.session() as session:
            try:
                category = self._repo.update(
                    session=session,
                    category_id=category_id,
                    data=data
                )
            except CategoryNotFoundException:
                error = CategoryNotFoundByIdException(id=category_id)
                logger.error(error.get_detail())
                raise error
            except CategoryTitleAlreadyExistsException:
                error = CategoryTitleIsNotUniqueException(title=data.title)
                logger.error(error.get_detail())
                raise error
            except CategorySlugAlreadyExistsException:
                error = CategorySlugIsNotUniqueException(slug=data.slug)
                logger.error(error.get_detail())
                raise error
            
            return CategoryResponse.model_validate(obj=category)
