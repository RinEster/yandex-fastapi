import logging

from application.core.exceptions.database_exceptions import (
    PostNotFoundException,
    NotPostAuthorException,
    PostImageNotFoundException
)
from application.core.exceptions.domain_exception import (
    PostNotFoundByIdException,
    NotPostAuthorDomainException,
PostHasNoImageIdException

)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import (
    PostRepository,
)

logger = logging.getLogger(__name__)


class DeleteSingleImageUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int, image_id: int, user_id: int) -> None:
        async with self._database.session() as session:
            try:
                await self._repo.delete_single_image(
                    session=session, post_id=post_id, image_id=image_id,user_id=user_id

                )
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=post_id)
                logger.error(error.get_detail())
                raise error
            except NotPostAuthorException:
                error = NotPostAuthorDomainException()
                logger.error(error.get_detail())
                raise error
            except PostImageNotFoundException:
                error = PostHasNoImageIdException(id=post_id)
                logger.error(error.get_detail())
                raise error
