import logging

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import UserResponse
from core.exceptions.database_exceptions import UserNotFoundException
from core.exceptions.domain_exception import UserNotFoundByLoginException

logger = logging.getLogger(__name__)


class GetUserByLoginUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, login: str) -> UserResponse:
        with self._database.session() as session:
            try:
                user = self._repo.get_user_by_login(session, login)
            except UserNotFoundException:
                error = UserNotFoundByLoginException(login=login)
                logger.error(error.get_detail())
                raise error

            return UserResponse.model_validate(obj=user)
