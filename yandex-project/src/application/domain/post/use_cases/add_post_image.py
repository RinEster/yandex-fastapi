from pathlib import Path

from application.core.exceptions.domain_exception import (
    UploadFileIsNotImageException,
)
from application.infrastructure.postgres.repositories.posts import (
    PostRepository,
)
from application.schemas.posts import PostResponse

from application.infrastructure.postgres.database import database

class AddPostImageUseCase:

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
    ) -> PostResponse:

        async with self._database.session() as session:
            extension = Path(image_path).suffix.lower()

            if extension not in self.ALLOWED_EXTENSIONS:
                raise UploadFileIsNotImageException()

            post = await self._repo.add_post_image(
                session=session,
                post_id=post_id,
                image_path=image_path,
            )

        return PostResponse.model_validate(post)
