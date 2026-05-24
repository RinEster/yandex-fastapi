from typing import List

from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import (
    PostRepository,
)
from application.schemas.posts import PostResponse


class GetPublishedPostsUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, limit: int = 15) -> List[PostResponse]:
        async with self._database.session() as session:
            posts = await self._repo.get_published(
                session=session, limit=limit
            )
            return [PostResponse.model_validate(obj=p) for p in posts]
