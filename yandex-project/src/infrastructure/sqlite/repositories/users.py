from typing import List, Type

from sqlalchemy.orm import Session

from infrastructure.sqlite.models.users import User


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User


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
        return query.scalar()

    def get_user_by_login(
        self,
        session: Session,
        login: str
    ) -> User:
        query = (
            session.query(self._model)
            .where(self._model.login == login)
        )
        return query.scalar()

    def get_user_by_email(
        self,
        session: Session,
        email: str
    ) -> User:
        query = (
            session.query(self._model)
            .where(self._model.email == email)
        )
        return query.scalar()

    def create(
        self,
        session:Session,
        login: str,
        email: str,
        password: str,
        first_name: str | None = None,
        second_name: str | None = None
    ) -> User:
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
        if user:
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
        if user:
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
        if user:
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
        if user:
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
    ) -> bool:
        user = self.get_user_by_id(session, user_id)
        if user:
            session.delete(user)
            session.flush()
            return True
        return False


