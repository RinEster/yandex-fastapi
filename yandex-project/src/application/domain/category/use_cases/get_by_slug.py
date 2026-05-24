import logging

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
)
from application.core.exceptions.domain_exception import (
    CategoryNotFoundBySlugException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.categories import (
    CategoryRepository,
)
from application.schemas.categories import CategoryResponse

logger = logging.getLogger(__name__)


class GetCategoryBySlugUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, slug: str) -> CategoryResponse:
        async with self._database.session() as session:
            try:
                category = await self._repo.get_by_slug(session, slug)
            except CategoryNotFoundException:
                error = CategoryNotFoundBySlugException(slug=slug)
                logger.error(error.get_detail())
                raise error

            return CategoryResponse.model_validate(obj=category)
