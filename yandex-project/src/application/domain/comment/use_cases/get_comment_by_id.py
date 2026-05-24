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
from application.schemas.comments import CommentResponse

logger = logging.getLogger(__name__)


class GetCommentByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> CommentResponse:
        async with self._database.session() as session:
            try:
                comment = await self._repo.get_by_id(
                    session=session, comment_id=comment_id
                )
                return CommentResponse.model_validate(obj=comment)
            except CommentNotFoundException:
                error = CommentNotFoundByIdException(id=comment_id)
                logger.error(error.get_detail())
                raise error
