from typing import Type, List

from sqlalchemy.orm import Session
from sqlalchemy import  select, or_, insert
from infrastructure.sqlite.models.users import User
from resources.auth import get_password_hash
from core.exceptions.database_exceptions import (
    UserNotFoundException,
    UserLoginAlreadyExistsException,
    UserEmailAlreadyExistsException
)

from schemas.users import UserCreate


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User

    def check_email_exists(
        self,
        session: Session,
        email: str
    ) -> bool:
        query = (
           session.query(self._model)
            .where(self._model.email == email)
        )
        user = query.scalar()
        return user is not None

    def chech_login_exists(
        self,
        session: Session,
        login: str
    ) -> bool:
        query = (
           session.query(self._model)
            .where(self._model.login == login)
        )
        user = query.scalar()
        return user is not None

    def get_all_user(
        self,
        session: Session
    ) -> List[User]:
        query = (
            session.query(self._model).all()
        )

        return query

    def get_user_by_id(
        self,
        session: Session,
        user_id: int
    ) -> User:
        query = (
            session.query(self._model)
            .where(self._model.id == user_id)
        )

        user = query.scalar()

        if not user:
            raise UserNotFoundException()

        return user

    def get_user_by_login(
        self,
        session: Session,
        login: str
    ) -> User:
        query = (
            session.query(self._model)
            .where(self._model.login == login)
        )
        user = query.scalar()
        if not user:
            raise UserNotFoundException()
        return user

    def get_user_by_email(
        self,
        session: Session,
        email: str
    ) -> User:
        query = (
            session.query(self._model)
            .where(self._model.email == email)
        )
        user = query.scalar()
        if not user:
            raise UserNotFoundException()
        return user

    def create(
        self,
        session: Session,
        data: UserCreate    
    ) -> User:

        exist_user = session.scalar(
            select(self._model).where(
                or_(self._model.login == data.login,
                    self._model.email == data.email,)
            )
        )

        if exist_user is not None:
            if exist_user.login == data.login:
                raise UserLoginAlreadyExistsException()
            if exist_user.email == data.email:
                raise UserEmailAlreadyExistsException()

        password = data.password.get_secret_value()
        hashed_password = get_password_hash(password)

        user_data = data.model_dump(exclude={"password"})
        user_data["password"] = hashed_password

        query = (
            insert(self._model)
            .values(user_data)
            .returning(self._model)
        )

        user = session.scalar(query)
        session.flush()

        return user

   
    def delete(
            self,
            session: Session,
            user_id: int
    ) -> None:
        user = self.get_user_by_id(session, user_id)
        session.delete(user)
        session.flush()
