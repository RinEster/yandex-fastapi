import logging

from application.core.exceptions.database_exceptions import (
    UserNotFoundException,
    UserLoginAlreadyExistsException,
    UserEmailAlreadyExistsException,
)
from application.core.exceptions.domain_exception import (
    UserNotFoundByIdException,
    UserLoginIsNotUniqueException,
    UserEmailIsNotUniqueException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.users import UserRepository
from application.schemas.users import UserResponse, UserUpdate

logger = logging.getLogger(__name__)


class UpdateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, data: UserUpdate) -> UserResponse:
        async with self._database.session() as session:
            try:
                user = await self._repo.update(
                    session=session, user_id=user_id, data=data
                )
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=user_id)
                logger.error(error.get_detail())
                raise error
            except UserLoginAlreadyExistsException:
                error = UserLoginIsNotUniqueException(login=(data.login or ""))
                logger.error(error.get_detail())
                raise error
            except UserEmailAlreadyExistsException:
                error = UserEmailIsNotUniqueException(email=(data.email or ""))
                logger.error(error.get_detail())
                raise error

        return UserResponse.model_validate(obj=user)
