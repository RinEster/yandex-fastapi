from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategoryResponse
from core.exceptions.database_exceptions import CategoryNotFoundException
from core.exceptions.domain_exception import CategoryNotFoundByIdException
import logging

logger = logging.getLogger(__name__)

class GetCategoryByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> CategoryResponse:
        with self._database.session() as session:
            try:
                category = self._repo.get_by_id(session, category_id)
            except CategoryNotFoundException:
                error = CategoryNotFoundByIdException(id=category_id)
                logger.error(error.get_detail())
                raise error
            
            return CategoryResponse.model_validate(obj=category)
