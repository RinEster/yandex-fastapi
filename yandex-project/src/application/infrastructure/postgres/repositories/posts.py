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

class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post
        self._author_model: Type[User] = User
        self._location_model: Type[Location] = Location
        self._category_model: Type[Category] = Category

    async def get_all(
            self,
            session: AsyncSession
    ) -> List[Post]:
        query = select(self._model)
        result = await session.execute(query)
        return list(result.scalars().all())
    
    async def get_published(
        self,
        session:AsyncSession,
        limit: int = 15
    ) -> List[Post]:
        query = (
            select(self._model)
            .where(self._model.is_published.is_(True))
            .order_by(self._model.pub_date.desc())
            .limit(limit)   
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(
        self,
        session: AsyncSession,
        post_id: int
    ) -> Post:
        query = (
            select(self._model)
            .where(self._model.id == post_id)
        )
        post = await session.execute(query)
        result = post.scalar()
        if not result:
            raise PostNotFoundException()
        return result

    async def create(
        self,
        session: AsyncSession,
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
        await session.add(post)
        await session.flush()
        return post

    async def update(
        self,
        session: AsyncSession,
        post_id: int,
        title: str,
        text: str,
        author_id: int,
        location_id: int,
        category_id: int,
        image: str,
        is_published: bool
    ) -> Post:
        post = await self.get_by_id(session, post_id)
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
            await session.flush()
        return post

    async def delete(
        self,
        session: AsyncSession,
        post_id: int
    ) -> None:
        post = await self.get_by_id(session, post_id)
        await session.delete(post)
        await session.flush()
