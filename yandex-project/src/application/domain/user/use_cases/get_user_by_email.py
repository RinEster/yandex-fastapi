import logging
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.users import UserRepository
from application.schemas.users import UserResponse
from application.core.exceptions.database_exceptions import UserNotFoundException
from application.core.exceptions.domain_exception import UserNotFoundByEmailException

logger = logging.getLogger(__name__)


class GetUserByEmailUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, email: str) -> UserResponse:
        async with self._database.session() as session:
            try:
                user = await self._repo.get_user_by_email(session=session, email=email)
                return UserResponse.model_validate(obj=user)
            except UserNotFoundException:
                error = UserNotFoundByEmailException(email=email)
                logger.error(error.get_detail())
                raise error
