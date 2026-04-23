import logging

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import UserCreate, UserResponse

from core.exceptions.database_exceptions import (
    UserLoginAlreadyExistsException as DBLoginException,
    UserEmailAlreadyExistsException as DBEmailException,
)

from core.exceptions.domain_exception import (
    UserLoginAlreadyExistsException,
    UserEmailAlreadyExistsException,
)

logger = logging.getLogger(__name__)


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, data: UserCreate) -> UserResponse:
        with self._database.session() as session:
            try:
                user = self._repo.create(
                    session=session,
                    data=data
                )

            except DBLoginException:
                error = UserLoginAlreadyExistsException(login=data.login)
                logger.error(error.get_detail())
                raise error

            except DBEmailException:
                error = UserEmailAlreadyExistsException(email=data.email)
                logger.error(error.get_detail())
                raise error

            return UserResponse.model_validate(obj=user)
