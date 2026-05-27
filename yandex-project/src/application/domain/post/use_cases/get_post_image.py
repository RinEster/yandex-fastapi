
from application.core.exceptions.domain_exception import (
    PostHasNoImageException,
)
from application.infrastructure.postgres.repositories.posts import (
    PostRepository,
)

from application.infrastructure.postgres.database import database

class GetPostImageUseCase:

    def __init__(self):
        self._repo = PostRepository()
        self._database = database
    async def execute(
        self,
        post_id: int,
    ) -> str:

        async with self._database.session() as session:
            image = await self._repo.get_post_image(
                session=session,
                post_id=post_id,
            )

            if not image:
                raise PostHasNoImageException()

        return image
