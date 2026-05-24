import logging

from application.core.exceptions.database_exceptions import (
    PostNotFoundException,
    UserNotFoundException,
)
from application.core.exceptions.domain_exception import (
    PostNotFoundByIdException,
    UserNotFoundByIdException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.comments import (
    CommentRepository,
)
from application.schemas.comments import (
    CommentCreate,
    CommentResponse,
)

logger = logging.getLogger(__name__)


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self, author_id: int, data: CommentCreate
    ) -> CommentResponse:
        async with self._database.session() as session:
            try:
                comment = await self._repo.create(
                    session=session, author_id=author_id, data=data
                )
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=data.post_id)
                logger.error(error.get_detail())
                raise error
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=author_id)
                logger.error(error.get_detail())
                raise error

            return CommentResponse.model_validate(obj=comment)
