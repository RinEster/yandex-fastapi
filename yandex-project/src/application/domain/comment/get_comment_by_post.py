from typing import List

from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.comments import (
    CommentRepository,
)
from application.schemas.comments import CommentResponse


class GetCommentsByPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, post_id: int) -> List[CommentResponse]:
        async with self._database.session() as session:
            comments = await self._repo.get_by_post_id(
                session=session, post_id=post_id
            )
            return [
                CommentResponse.model_validate(obj=c)
                for c in comments
            ]
