from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.posts import PostRepository
from application.schemas.page import Page
from application.schemas.posts import PostResponse


class GetUserBookmarksUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, user_id: int, page: int, size: int) -> Page[PostResponse]:
        async with self._database.session() as session:
            pagination_data = await self._repo.get_user_bookmarks(
                session=session, user_id=user_id, page=page, size=size
            )
            return Page[PostResponse].model_validate(pagination_data)
