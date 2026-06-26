import logging
from typing import List

from application.core.exceptions.database_exceptions import CommentNotFoundException
from application.core.exceptions.domain_exception import (
    CommentNotFoundByIdException,
    CommentHasNoImageException,  # Если комментарий пустой, можно бросить доменную ошибку
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.comments import (
    CommentRepository,
)
from application.schemas.comments import CommentImageResponse

logger = logging.getLogger(__name__)


class GetCommentImagesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> List[CommentImageResponse]:
        async with self._database.session() as session:
            try:
                images = await self._repo.get_comment_images(
                    session=session, comment_id=comment_id
                )
            except CommentNotFoundException:
                error = CommentNotFoundByIdException(id=comment_id)
                logger.error(error.get_detail())
                raise error

            return [CommentImageResponse.model_validate(img) for img in images]
