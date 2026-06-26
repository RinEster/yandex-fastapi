import logging
from pathlib import Path

from application.core.exceptions.database_exceptions import UserNotFoundException
from application.core.exceptions.domain_exception import (
    UserNotFoundByIdException,
    UploadFileIsNotImageException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.users import UserRepository
from application.schemas.users import UserResponse

logger = logging.getLogger(__name__)


class UploadAvatarUseCase:
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, image_path: str) -> UserResponse:
        # Проверяем расширение файла перед обращением к БД
        extension = Path(image_path).suffix.lower()
        if extension not in self.ALLOWED_EXTENSIONS:
            raise UploadFileIsNotImageException()

        async with self._database.session() as session:
            try:
                user = await self._repo.update_avatar(
                    session=session, user_id=user_id, avatar_path=image_path
                )
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=user_id)
                logger.error(error.get_detail())
                raise error

        return UserResponse.model_validate(obj=user)
