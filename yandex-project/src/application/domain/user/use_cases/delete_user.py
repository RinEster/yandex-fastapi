import logging

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from core.exceptions.database_exceptions import UserNotFoundException
from core.exceptions.domain_exception import UserNotFoundByIdException

logger = logging.getLogger(__name__)


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> None:
        with self._database.session() as session:
            try:
                self._repo.delete(session, user_id)
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=user_id)
                logger.error(error.get_detail())
                raise error
