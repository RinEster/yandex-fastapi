from application.infrastructure.postgres.database import database

import logging
from application.infrastructure.postgres.repositories.posts import (
    PostRepository,
)
from application.schemas.page import Page  
from application.schemas.posts import PostResponse
from application.core.exceptions.database_exceptions import CategoryNotFoundException
from application.core.exceptions.domain_exception import CategoryNotFoundByIdException

logger = logging.getLogger(__name__)
class GetPostsByCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, category_id: int, page: int = 1, size: int = 15) -> Page[PostResponse]:
        async with self._database.session() as session:
            
            try:
                pagination_dict = await self._repo.get_all_by_category(
                    session=session, 
                    category_id=category_id,
                    page=page, 
                    size=size
                )
            except CategoryNotFoundException:
                error = CategoryNotFoundByIdException(id=category_id)
                logger.error(error.get_detail())
                raise error
            return Page[PostResponse].model_validate(pagination_dict)
