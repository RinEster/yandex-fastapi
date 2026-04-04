from typing import List, Type

from sqlalchemy.orm import Session

from infrastructure.sqlite.models.users import User

from core.exceptions.database_exceptions import(
    UserNotFoundException,
    UserLoginAlreadyExistsException,
    UserEmailAlreadyExistsException
)

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

        if not query:
            raise UserNotFoundException

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
            raise UserNotFoundException

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
            raise UserNotFoundException
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
            raise UserNotFoundException
        return user

    def create(
        self,
        session:Session,
        login: str,
        email: str,
        password: str,
        first_name: str | None = None,
        second_name: str | None = None
    ) -> User:

        if self.chech_login_exists(session,login):
            raise UserLoginAlreadyExistsException

        if self.check_email_exists(session, email):
            raise UserEmailAlreadyExistsException

        user = User(
            login=login,
            email=email,
            password=password,
            first_name=first_name,
            second_name=second_name
        )
        session.add(user)
        session.flush()
        return user

    def update_login(
        self,
        session: Session,
        user_id: int,
        new_login: str
    ) -> User:
        user = self.get_user_by_id(session, user_id)
        
        if self.chech_login_exists(session, new_login):
            existing_user = (
                session.query(self._model)
                .where(self._model.login == new_login)
                .scalar()
            )
            if existing_user and existing_user.id != user_id:
                raise UserLoginAlreadyExistsException

        user.login = new_login
        session.flush()

        return user
    
    def update_email(
        self, 
        session: Session,
        user_id: int,
        new_email: str
    ) -> User:
        user = self.get_user_by_id(session, user_id)
        
        if self.check_email_exists(session, new_email):
            existing_user = (
                session.query(self._model)
                .where(self._model.email == new_email)
                .scalar()
            )
            if existing_user and existing_user.id != user_id:
                raise UserEmailAlreadyExistsException
        
        user.email = new_email
        session.flush()
        return user
    
    def update_password(
        self,
        session: Session,
        user_id: int,
        new_password: str
    ) -> User:
        user = self.get_user_by_id(session, user_id)
        user.password = new_password
        session.flush()
        return user
    
    def update_name(
        self,
        session: Session,
        user_id: int,
        first_name: str | None = None,
        second_name: str | None = None
    ) -> User:
        user = self.get_user_by_id(session, user_id)
        if first_name is not None:
            user.first_name = first_name
        if second_name is not None:
            user.second_name = second_name
        session.flush()
        return user

    def delete_user(
        self,
        session: Session,
        user_id: int
    ) -> None:
        user = self.get_user_by_id(session, user_id)
        if user:
            session.delete(user)
            session.flush()
        else:
            raise UserNotFoundException


