import logging
from pathlib import Path
from typing import List

from application.core.exceptions.database_exceptions import (
    PostNotFoundException,
    NotPostAuthorException,
)
from application.core.exceptions.domain_exception import (
    PostNotFoundByIdException,
    NotPostAuthorDomainException,
    UploadFileIsNotImageException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import (
    PostRepository,
)
from application.schemas.posts import PostResponse

logger = logging.getLogger(__name__)


class AddPostImagesUseCase:

    ALLOWED_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
    }

    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self,
        post_id: int,
        image_path: str,
        user_id: int
    ) -> PostResponse:

        extension = Path(image_path).suffix.lower()
        if extension not in self.ALLOWED_EXTENSIONS:
            raise UploadFileIsNotImageException()

        async with self._database.session() as session:
            try:
                post = await self._repo.add_post_images(
                    session=session,
                    post_id=post_id,
                    image_url=image_path,
                    user_id=user_id,
                )
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=post_id)
                logger.error(error.get_detail())
                raise error
            except NotPostAuthorException:
                error = NotPostAuthorDomainException()
                logger.error(error.get_detail())
                raise error

        return PostResponse.model_validate(post)
