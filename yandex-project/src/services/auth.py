from typing import Annotated
from fastapi import Depends
from pydantic import SecretStr
from jose import JWTError, jwt

from core.exceptions.auth_exceptions import CredentialsException
from core.exceptions.database_exceptions import UserNotFoundException
from schemas.users import UserResponse as UserSchema
from resources.auth import oauth2_scheme
from infrastructure.sqlite.database import (
    database as sqlite_database,
    Database,
)
from infrastructure.sqlite.repositories.users import UserRepository

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

        try:
            with _database.session() as session:
                user = _repo.get_user_by_login(session=session, login=login)
        except UserNotFoundException:
            raise CredentialsException(detail="Пользователь не найден")

        return UserSchema.model_validate(obj=user)

    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> UserSchema:
        return await AuthService._resolve_user_from_token(token=token)
