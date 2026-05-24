import logging

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    LocationNotFoundException,
    PostNotFoundException,
)
from application.core.exceptions.domain_exception import (
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
    PostNotFoundByIdException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import (
    PostRepository,
)
from application.schemas.posts import PostResponse, PostUpdate

logger = logging.getLogger(__name__)


class UpdatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self, post_id: int, data: PostUpdate
    ) -> PostResponse:
        async with self._database.session() as session:
            try:
                post = await self._repo.update(
                    session=session, post_id=post_id, data=data
                )
                await session.commit()
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=post_id)
                logger.error(error.get_detail())
                raise error
            except CategoryNotFoundException:
                failed_id = data.category_id or 0
                error = CategoryNotFoundByIdException(id=failed_id)
                logger.error(error.get_detail())
                raise error
            except LocationNotFoundException:
                failed_id = data.location_id or 0
                error = LocationNotFoundByIdException(id=failed_id)
                logger.error(error.get_detail())
                raise error

            return PostResponse.model_validate(obj=post)
