from datetime import datetime
from typing import Type, List

from sqlalchemy.orm import Session

from infrastructure.sqlite.models.posts import Post


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post

    def get_all(self, session: Session) -> List[Post]:
        query = session.query(self._model).all()
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
        return query.scalar()

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
        session.commit()
        return post

    def update(
        self,
        session: Session,
        post_id: int,
        title: str,
        text: str,
        location_id: int,
        category_id: int,
        image: str,
        is_published: bool
    ) -> Post:
        post = self.get_by_id(session, post_id)
        if post:
            post.title=title
            post.text = text
            post.location_id = location_id
            post.category_id = category_id
            post.image = image
            post.is_published = is_published
            session.commit()
        return post

    def delete(
        self,
        session: Session,
        post_id: int
    ) -> bool:
        post = self.get_by_id(session, post_id)
        if post:
            session.delete(post)
            session.commit()
            return True
        return False
