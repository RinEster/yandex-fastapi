from typing import Annotated
from fastapi import Depends
from pydantic import SecretStr
from jose import JWTError, jwt

from application.core.exceptions.auth_exceptions import CredentialsException
from application.core.exceptions.database_exceptions import UserNotFoundException
from application.schemas.users import UserResponse
from application.resources.auth import oauth2_scheme
from application.infrastructure.sqlite.database import (
    database as postgres_database,
    Database,
)
from application.infrastructure.sqlite.repositories.users import UserRepository
from application.core.config import setting

AUTH_EXCEPTION_MESSAGE = "Невозможно проверить данные авторизации"
SECRET_AUTH_KEY = SecretStr("DCTswSgPQuM3zSRM4g9FUFM5EAOr8ypfFwg7pK2eVV8")
AUTH_ALGORITHM = "HS256"


class AuthService:
    @staticmethod
    async def _resolve_user_from_token(token: str) -> UserSchema:
        _database: Database = sqlite_database
        _repo: UserRepository = UserRepository()

        try:
            payload = jwt.decode(
                token=token,
                key=SECRET_AUTH_KEY.get_secret_value(),
                algorithms=[AUTH_ALGORITHM],
            )
            login = payload.get('sub')
            if login is None:
                raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)
        except JWTError:
            raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)

        with _database.session() as session:
            user = _repo.get_user_by_login(session=session, login=login)

            if not user:
                raise CredentialsException(detail="Пользователь не найден")

            return UserSchema.model_validate(user)

    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> UserSchema:
        return await AuthService._resolve_user_from_token(token=token)
