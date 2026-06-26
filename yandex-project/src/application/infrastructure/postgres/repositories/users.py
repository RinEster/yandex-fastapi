from typing import List, Type

from application.core.exceptions.database_exceptions import (
    UserEmailAlreadyExistsException,
    UserLoginAlreadyExistsException,
    UserNotFoundException,
)
from application.infrastructure.postgres.models.users import User
from application.resources.auth import get_password_hash
from application.schemas.users import UserCreate, UserUpdate
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User

    async def check_email_exists(
        self, session: AsyncSession, email: str
    ) -> bool:
        query = select(self._model).where(self._model.email == email)
        user = await session.scalar(query)
        return user is not None

    async def chech_login_exists(
        self, session: AsyncSession, login: str
    ) -> bool:
        query = select(self._model).where(self._model.login == login)
        user = await session.scalar(query)
        return user is not None

    async def get_all_user(self, session: AsyncSession) -> List[User]:
        query = select(self._model)
        result = await session.execute(query)
        return list(result.scalars().all())

    async def get_user_by_id(
        self, session: AsyncSession, user_id: int
    ) -> User:
        query = select(self._model).where(self._model.id == user_id)
        user = await session.scalar(query)
        if not user:
            raise UserNotFoundException()
        return user

    async def get_user_by_login(
        self, session: AsyncSession, login: str
    ) -> User:
        query = select(self._model).where(self._model.login == login)
        user = await session.scalar(query)
        if not user:
            raise UserNotFoundException()
        return user

    async def get_user_by_email(
        self, session: AsyncSession, email: str
    ) -> User:
        query = select(self._model).where(self._model.email == email)
        user = await session.scalar(query)
        if not user:
            raise UserNotFoundException()
        return user

    async def create(
        self, session: AsyncSession, data: UserCreate
    ) -> User:

        exist_user = await session.scalar(
            select(self._model).where(
                or_(
                    self._model.login == data.login,
                    self._model.email == data.email,
                )
            )
        )

        if exist_user is not None:
            if exist_user.login == data.login:
                raise UserLoginAlreadyExistsException(login=data.login)
            if exist_user.email == data.email:
                raise UserEmailAlreadyExistsException(email=data.email)

        password = data.password.get_secret_value()
        hashed_password = get_password_hash(password)

        user_data = data.model_dump(exclude={"password"})
        user_data["password"] = hashed_password

        user = self._model(**user_data)
        session.add(user)
        await session.flush()

        return user

    async def update(
        self, session: AsyncSession, user_id: int, data: UserUpdate
    ) -> User:
        user = await self.get_user_by_id(session, user_id)

        if data.login is not None and data.login != user.login:
            if await self.chech_login_exists(session, data.login):
                raise UserLoginAlreadyExistsException(login=data.login)

        if data.email is not None and data.email != user.email:
            if await self.check_email_exists(session, data.email):
                raise UserEmailAlreadyExistsException(email=data.email)

        update_data = data.model_dump(
            exclude_none=True, exclude={"password"}
        )

        if data.password is not None:
            raw_password = data.password.get_secret_value()
            update_data["password"] = get_password_hash(raw_password)

        for key, value in update_data.items():
            setattr(user, key, value)

        await session.flush()
        return user

    async def delete(
        self, session: AsyncSession, user_id: int
    ) -> None:
        user = await self.get_user_by_id(session, user_id)
        await session.delete(user)
        await session.flush()

    async def update_avatar(
        self, session: AsyncSession, user_id: int, avatar_path: str
    ) -> User:
        user = await self.get_user_by_id(session, user_id)
        user.avatar = avatar_path
        await session.flush()
        return user

    async def delete_avatar(
        self, session: AsyncSession, user_id: int
    ) -> User:
        user = await self.get_user_by_id(session, user_id)
        user.avatar = None
        await session.flush()
        return user
