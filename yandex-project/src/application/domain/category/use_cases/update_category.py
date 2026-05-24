import logging

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    CategorySlugAlreadyExistsException,
    CategoryTitleAlreadyExistsException,
)
from application.core.exceptions.domain_exception import (
    CategoryNotFoundByIdException,
    CategorySlugIsNotUniqueException,
    CategoryTitleIsNotUniqueException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.categories import (
    CategoryRepository,
)
from application.schemas.categories import (
    CategoryResponse,
    CategoryUpdate,
)

logger = logging.getLogger(__name__)


class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self, category_id: int, data: CategoryUpdate
    ) -> CategoryResponse:
        async with self._database.session() as session:
            try:
                category = await self._repo.update(
                    session=session,
                    category_id=category_id,
                    data=data,
                )
            except CategoryNotFoundException:
                error = CategoryNotFoundByIdException(id=category_id)
                logger.error(error.get_detail())
                raise error
            except CategoryTitleAlreadyExistsException as e:
                failed_title = data.title or getattr(
                    e, "title", "Указанный заголовок"
                )
                error = CategoryTitleIsNotUniqueException(
                    title=failed_title
                )
                logger.error(error.get_detail())
                raise error
            except CategorySlugAlreadyExistsException as e:
                failed_slug = data.slug or getattr(
                    e, "slug", "Указанный slug"
                )
                error = CategorySlugIsNotUniqueException(
                    slug=failed_slug
                )
                logger.error(error.get_detail())
                raise error

            return CategoryResponse.model_validate(obj=category)
