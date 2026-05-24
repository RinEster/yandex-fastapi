import logging

from application.core.exceptions.database_exceptions import (
    PostNotFoundException,
)
from application.core.exceptions.domain_exception import (
    PostNotFoundByIdException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import (
    PostRepository,
)

logger = logging.getLogger(__name__)


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> None:
        async with self._database.session() as session:
            try:
                await self._repo.delete(
                    session=session, post_id=post_id
                )
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=post_id)
                logger.error(error.get_detail())
                raise error
