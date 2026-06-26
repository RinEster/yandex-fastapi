import logging
from typing import List

from application.core.exceptions.database_exceptions import PostNotFoundException
from application.core.exceptions.domain_exception import (
    PostNotFoundByIdException,
    PostHasNoImageException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import (
    PostRepository,
)
from application.schemas.posts import PostImageResponse

logger = logging.getLogger(__name__)


class GetPostImagesUseCase:

    def __init__(self):
        self._repo = PostRepository()
        self._database = database

    async def execute(
        self,
        post_id: int,
    ) -> List[PostImageResponse]:

        async with self._database.session() as session:
            try:
                images = await self._repo.get_post_images(
                    session=session,
                    post_id=post_id,
                )
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=post_id)
                logger.error(error.get_detail())
                raise error

            if not images:
                raise PostHasNoImageException()

            return [PostImageResponse.model_validate(img) for img in images]
