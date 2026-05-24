import logging
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.users import UserRepository
from application.schemas.users import UserResponse
from application.core.exceptions.database_exceptions import UserNotFoundException
from application.core.exceptions.domain_exception import UserNotFoundByIdException

logger = logging.getLogger(__name__)


class GetUserByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> UserResponse:
        async with self._database.session() as session:
            try:
                user = await self._repo.get_user_by_id(session=session, user_id=user_id)
                return UserResponse.model_validate(obj=user)
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=user_id)
                logger.error(error.get_detail())
                raise error
