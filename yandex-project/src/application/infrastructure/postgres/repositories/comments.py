
from datetime import datetime
from typing import Type, List


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.infrastructure.postgres.models.comments import Comment
from application.infrastructure.postgres.models.posts import Post
from application.infrastructure.postgres.models.categories import Category
from application.infrastructure.postgres.models.locations import Location
from application.infrastructure.postgres.models.users import User
from application.core.exceptions.database_exceptions import(
    PostNotFoundException,
    CategoryNotFoundException,
    LocationNotFoundException,
    UserNotFoundException,
    CommentNotFoundException
)


class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment
        self._post_model: Type[Post] = Post
        self._author_model: Type[User] = User

    def get_all(
        self,
        session: Session
    ) -> List[Comment]:
        query = session.query(self._model).all()
        return query
    
    def get_by_id(
        self,
        session: Session,
        comment_id: int
    ) -> Comment:
        query = (
            session.query(self._model)
            .where(self._model.id == comment_id)
        )
        comment = query.scalar()
        if not comment:
            raise CommentNotFoundException()
        return comment

    def get_by_post_id(
        self,
        session: Session,
        post_id: int
    ) -> List[Comment]:
        query = (
            session.query(self._model)
            .where(self._model.post_id == post_id)
            .order_by(self._model.created_at.desc())
            .all()
        )
        return query

    def get_by_author_id(
        self,
        session: Session,
        author_id: int
    ) -> List[Comment]:
        query = (
            session.query(self._model)
            .where(self._model.author_id == author_id)
            .order_by(self._model.created_at.desc())
            .all()
        )
        return query

    def create(
        self,
        session: Session,
        post_id: int,
        author_id: int,
        text: str
    ) -> Comment:
        post = session.get(self._post_model, post_id)
        if not post:
            raise PostNotFoundException()
        
        author = session.get(self._author_model, author_id)
        if not author:
            raise UserNotFoundException()

        comment = self._model(
            post_id=post_id,
            author_id=author_id,
            text=text,
            created_at=datetime.now()
        )
        session.add(comment)
        session.flush()
        return comment

    def update(
        self,
        session: Session,
        comment_id: int,
        text: str
    ) -> Comment:
        comment = self.get_by_id(session, comment_id)
        
        comment.text = text
        session.flush()
        
        return comment

    def delete(
        self,
        session: Session,
        comment_id: int
    ) -> None:
        comment = self.get_by_id(session, comment_id)
        session.delete(comment)
        session.flush()

