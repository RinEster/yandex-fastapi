import logging

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import UserResponse
from resources.auth import verify_password
from core.exceptions.database_exceptions import UserNotFoundException
from core.exceptions.domain_exception import UserNotFoundByLoginException, WrongPasswordException

logger = logging.getLogger(__name__)


class AuthenticateUserUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self,
        login: str,
        password: str,
    ) -> UserResponse:
        try:
            with self._database.session() as session:
                user = self._repo.get_user_by_login(
                    session=session,
                    login=login
                )

                if not verify_password(
                    plain_password=password,
                    hashed_password=user.password
                ):
                    error = WrongPasswordException()
                    logger.error(error.get_detail())
                    raise error

                return UserResponse.model_validate(user)

        except UserNotFoundException:
            error = UserNotFoundByLoginException(login=login)
            logger.error(error.get_detail())
            raise error
