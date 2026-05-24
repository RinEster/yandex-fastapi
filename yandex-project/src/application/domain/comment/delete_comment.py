import logging

from application.core.exceptions.database_exceptions import (
    CommentNotFoundException,
)
from application.core.exceptions.domain_exception import (
    CommentNotFoundByIdException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.comments import (
    CommentRepository,
)

logger = logging.getLogger(__name__)


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> None:
        async with self._database.session() as session:
            try:
                await self._repo.delete(
                    session=session, comment_id=comment_id
                )
                await session.commit()
            except CommentNotFoundException:
                error = CommentNotFoundByIdException(id=comment_id)
                logger.error(error.get_detail())
                raise error
