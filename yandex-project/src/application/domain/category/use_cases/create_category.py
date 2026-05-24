import logging

from application.core.exceptions.database_exceptions import (
    CategorySlugAlreadyExistsException,
    CategoryTitleAlreadyExistsException,
)
from application.core.exceptions.domain_exception import (
    CategorySlugIsNotUniqueException,
    CategoryTitleIsNotUniqueException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.categories import (
    CategoryRepository,
)
from application.schemas.categories import (
    CategoryCreate,
    CategoryResponse,
)

logger = logging.getLogger(__name__)


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, data: CategoryCreate) -> CategoryResponse:
        async with self._database.session() as session:
            try:
                category = await self._repo.create(
                    session=session, data=data
                )
            except CategoryTitleAlreadyExistsException:
                error = CategoryTitleIsNotUniqueException(
                    title=data.title
                )
                logger.error(error.get_detail())
                raise error
            except CategorySlugAlreadyExistsException:
                error = CategorySlugIsNotUniqueException(
                    slug=data.slug
                )
                logger.error(error.get_detail())
                raise error
            return CategoryResponse.model_validate(obj=category)
