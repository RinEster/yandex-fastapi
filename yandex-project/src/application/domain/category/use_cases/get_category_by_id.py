import logging

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
)
from application.core.exceptions.domain_exception import (
    CategoryNotFoundByIdException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.categories import (
    CategoryRepository,
)
from application.schemas.categories import CategoryResponse

logger = logging.getLogger(__name__)


class GetCategoryByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> CategoryResponse:
        async with self._database.session() as session:
            try:
                category = await self._repo.get_by_id(
                    session, category_id
                )
            except CategoryNotFoundException:
                error = CategoryNotFoundByIdException(id=category_id)
                logger.error(error.get_detail())
                raise error

            return CategoryResponse.model_validate(obj=category)
