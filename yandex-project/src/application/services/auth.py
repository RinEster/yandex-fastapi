from typing import Annotated
from fastapi import Depends
from pydantic import SecretStr
from jose import JWTError, jwt

from application.core.exceptions.auth_exceptions import CredentialsException
from application.schemas.users import UserResponse as UserSchema 
from application.resources.auth import oauth2_scheme
from application.infrastructure.postgres.database import database as postgres_database
from application.infrastructure.postgres.repositories.users import UserRepository
from application.core.config import settings

AUTH_EXCEPTION_MESSAGE = "Невозможно проверить данные авторизации"
SECRET_AUTH_KEY = SecretStr("0c540f6dd70f6a4582b87147c88ec7f71040e4656aec4aef591f69cc874c122f") 
AUTH_ALGORITHM = "HS256"

class AuthService:
    @staticmethod
    async def _resolve_user_from_token(token: str) -> UserSchema:
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

        async with postgres_database.session() as session:
            user = await _repo.get_user_by_login(session=session, login=login)

            if not user:
                raise CredentialsException(detail="Пользователь не найден")

            return UserSchema.model_validate(user)

    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> UserSchema:
        return await AuthService._resolve_user_from_token(token=token)
