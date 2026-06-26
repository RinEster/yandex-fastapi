import logging

from application.core.exceptions.database_exceptions import PostNotFoundException
from application.core.exceptions.domain_exception import PostNotFoundByIdException
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import PostRepository

logger = logging.getLogger(__name__)


class ToggleBookmarkUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int, user_id: int) -> bool:
        async with self._database.session() as session:
            try:
                return await self._repo.toggle_bookmark(
                    session=session, post_id=post_id, user_id=user_id
                )
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=post_id)
                logger.error(error.get_detail())
                raise error
