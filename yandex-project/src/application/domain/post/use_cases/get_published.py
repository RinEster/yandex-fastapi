from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import (
    PostRepository,
)
from application.schemas.page import Page  
from application.schemas.posts import PostResponse


class GetPublishedPostsUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, page: int = 1, size: int = 15) -> Page[PostResponse]:
        async with self._database.session() as session:
            pagination_dict = await self._repo.get_published(
                session=session, 
                page=page, 
                size=size
            )
            
            return Page[PostResponse].model_validate(pagination_dict)
