import logging
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.users import UserRepository
from application.schemas.users import UserResponse
from application.core.exceptions.database_exceptions import UserNotFoundException
from application.core.exceptions.domain_exception import UserNotFoundByLoginException

logger = logging.getLogger(__name__)


class GetUserByLoginUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, login: str) -> UserResponse:
        async with self._database.session() as session:
            try:
                user = await self._repo.get_user_by_login(session=session, login=login)
                return UserResponse.model_validate(obj=user)
            except UserNotFoundException:
                error = UserNotFoundByLoginException(login=login)
                logger.error(error.get_detail())
                raise error
