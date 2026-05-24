import logging
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.users import UserRepository
from application.core.exceptions.database_exceptions import UserNotFoundException
from application.core.exceptions.domain_exception import UserNotFoundByIdException

logger = logging.getLogger(__name__)


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> None:
        async with self._database.session() as session:
            try:
                await self._repo.delete(session=session, user_id=user_id)
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=user_id)
                logger.error(error.get_detail())
                raise error
