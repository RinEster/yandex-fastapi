from datetime import datetime
from typing import Type, List

from sqlalchemy.orm import Session

from infrastructure.sqlite.models.posts import Post, Comment
from infrastructure.sqlite.models.categories import Category
from infrastructure.sqlite.models.locations import Location
from infrastructure.sqlite.models.users import User
from core.exceptions.database_exceptions import(
    PostNotFoundException,
    CategoryNotFoundException,
    LocationNotFoundException,
    UserNotFoundException,
    CommentNotFoundException
)

class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post
        self._author_model: Type[User] = User
        self._location_model: Type[Location] = Location
        self._category_model: Type[Category] = Category

    def get_all(
            self,
            session: Session
    ) -> List[Post]:
        query = session.query(self._model).all()
        return query
    
    def get_published(
        self,
        session:Session,
        limit: int = 15
    ) -> List[Post]:
        query = (
            session.query(self._model)
            .where(self._model.is_published == True)
            .order_by(self._model.pub_date.desc())
            .limit(limit)   
        ).all()
        return query

    def get_by_id(
        self,
        session: Session,
        post_id: int
    ) -> Post:
        query = (
            session.query(self._model)
            .where(self._model.id == post_id)
        )
        post = query.scalar()
        if not post:
            raise PostNotFoundException()
        return post

    def create(
        self,
        session: Session,
        title: str,
        text: str,
        pub_date: datetime,
        author_id: int,
        location_id: int |None = None,
        category_id: int |None = None,
        image: str |None = None,
        is_published: bool = True
    ) -> Post:
        author = session.get(self._author_model, author_id)
        if not author:
            raise UserNotFoundException()

        category = session.get(self._category_model, category_id)
        if not category:
            raise CategoryNotFoundException()

        location = session.get(self._location_model,location_id)
        if not location:
            raise LocationNotFoundException()
            
        post = self._model(
            title=title,
            text=text,
            pub_date=pub_date,
            author_id=author_id,
            location_id=location_id,
            category_id=category_id,
            image=image,
            is_published=is_published,
            created_at=datetime.now()
        )
        session.add(post)
        session.flush()
        return post

    def update(
        self,
        session: Session,
        post_id: int,
        title: str,
        text: str,
        author_id: int,
        location_id: int,
        category_id: int,
        image: str,
        is_published: bool
    ) -> Post:
        post = self.get_by_id(session, post_id)
        author = session.get(self._author_model, author_id)
        if not author:
            raise UserNotFoundException()

        category = session.get(self._category_model, category_id)
        if not category:
            raise CategoryNotFoundException()

        location = session.get(self._location_model,location_id)
        if not location:
            raise LocationNotFoundException()

        if post:
            post.title=title
            post.text = text
            post.location_id = location_id
            post.category_id = category_id
            post.image = image
            post.is_published = is_published
            session.flush()
        return post

    def delete(
        self,
        session: Session,
        post_id: int
    ) -> None:
        post = self.get_by_id(session, post_id)
        session.delete(post)
        session.flush()

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

