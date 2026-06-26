import logging

from application.core.exceptions.database_exceptions import (
    PostNotFoundException,
    NotPostAuthorException
)
from application.core.exceptions.domain_exception import (
    PostNotFoundByIdException,
    NotPostAuthorDomainException
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import (
    PostRepository,
)

logger = logging.getLogger(__name__)


class DeleteAllImagesUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int, user_id: int) -> None:
        async with self._database.session() as session:
            try:
                await self._repo.delete_all_images(
                    session=session, post_id=post_id,user_id=user_id
                )
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=post_id)
                logger.error(error.get_detail())
                raise error
            except NotPostAuthorException:
                error = NotPostAuthorDomainException()
                logger.error(error.get_detail())
                raise error
