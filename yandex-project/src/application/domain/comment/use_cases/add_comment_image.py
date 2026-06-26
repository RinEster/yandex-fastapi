import logging
from pathlib import Path

from application.core.exceptions.database_exceptions import (
    CommentNotFoundException,
    NotCommentAuthor,
)
from application.core.exceptions.domain_exception import (
    CommentNotFoundByIdException,
    NotCommentAuthorDomainException,
    UploadFileIsNotImageException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.comments import (
    CommentRepository,
)
from application.schemas.comments import CommentResponse

logger = logging.getLogger(__name__)


class AddCommentImageUseCase:
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self,
        comment_id: int,
        image_path: str,
        user_id: int
    ) -> CommentResponse:
        extension = Path(image_path).suffix.lower()
        if extension not in self.ALLOWED_EXTENSIONS:
            raise UploadFileIsNotImageException()

        async with self._database.session() as session:
            try:
                comment = await self._repo.add_comment_image(
                    session=session,
                    comment_id=comment_id,
                    image_url=image_path,
                    user_id=user_id,
                )
            except CommentNotFoundException:
                error = CommentNotFoundByIdException(id=comment_id)
                logger.error(error.get_detail())
                raise error
            except NotCommentAuthor:
                error = NotCommentAuthorDomainException()
                logger.error(error.get_detail())
                raise error

        return CommentResponse.model_validate(obj=comment)
