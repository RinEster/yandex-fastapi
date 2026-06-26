import logging

from application.core.exceptions.database_exceptions import (
    CommentNotFoundException,
    NotCommentAuthor,
)
from application.core.exceptions.domain_exception import (
    CommentNotFoundByIdException,
    NotCommentAuthorDomainException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.comments import (
    CommentRepository,
)

logger = logging.getLogger(__name__)


class DeleteAllCommentImagesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int, user_id: int) -> None:
        async with self._database.session() as session:
            try:
                await self._repo.delete_all_images(
                    session=session, comment_id=comment_id, user_id=user_id
                )
            except CommentNotFoundException:
                error = CommentNotFoundByIdException(id=comment_id)
                logger.error(error.get_detail())
                raise error
            except NotCommentAuthor:
                error = NotCommentAuthorDomainException()
                logger.error(error.get_detail())
                raise error
