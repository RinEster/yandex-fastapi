import logging

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    LocationNotFoundException,
    UserNotFoundException,
)
from application.core.exceptions.domain_exception import (
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
    UserNotFoundByIdException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import (
    PostRepository,
)
from application.schemas.posts import PostCreate, PostResponse

logger = logging.getLogger(__name__)


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self, author_id: int, data: PostCreate
    ) -> PostResponse:
        async with self._database.session() as session:
            try:
                post = await self._repo.create(
                    session=session, author_id=author_id, data=data
                )
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=author_id)
                logger.error(error.get_detail())
                raise error
            except CategoryNotFoundException:
                failed_id = (
                    data.category_id
                    if data.category_id is not None
                    else 0
                )
                error = CategoryNotFoundByIdException(id=failed_id)
                logger.error(error.get_detail())
                raise error
            except LocationNotFoundException:
                failed_id = (
                    data.location_id
                    if data.location_id is not None
                    else 0
                )
                error = LocationNotFoundByIdException(id=failed_id)
                logger.error(error.get_detail())
                raise error

            return PostResponse.model_validate(obj=post)
