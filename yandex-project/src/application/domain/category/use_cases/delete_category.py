from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from core.exceptions.database_exceptions import CategoryNotFoundException
from core.exceptions.domain_exception import CategoryNotFoundByIdException
import logging

logger = logging.getLogger(__name__)
class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> None:
        with self._database.session() as session:
            try:
                self._repo.delete(session=session, category_id=category_id)
            except CategoryNotFoundException:
                error = CategoryNotFoundByIdException(id=category_id)
                logger.error(error.get_detail())
                raise error
