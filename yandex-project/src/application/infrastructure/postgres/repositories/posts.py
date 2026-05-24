from typing import List, Type

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    LocationNotFoundException,
    PostNotFoundException,
    UserNotFoundException,
)
from application.infrastructure.postgres.models.categories import (
    Category,
)
from application.infrastructure.postgres.models.locations import (
    Location,
)
from application.infrastructure.postgres.models.posts import Post
from application.infrastructure.postgres.models.users import User
from application.schemas.posts import PostCreate, PostUpdate
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post
        self._author_model: Type[User] = User
        self._location_model: Type[Location] = Location
        self._category_model: Type[Category] = Category

    def _get_base_query(self) -> Select:
        return select(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.category),
            joinedload(self._model.location),
            selectinload(self._model.comments),
        )

    async def get_all(self, session: AsyncSession) -> List[Post]:
        query = self._get_base_query()
        result = await session.execute(query)
        return list(result.scalars().all())

    async def get_published(
        self, session: AsyncSession, limit: int = 15
    ) -> List[Post]:
        query = (
            self._get_base_query()
            .where(self._model.is_published.is_(True))
            .order_by(self._model.pub_date.desc())
            .limit(limit)
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(
        self, session: AsyncSession, post_id: int
    ) -> Post:
        query = self._get_base_query().where(
            self._model.id == post_id
        )
        post = await session.execute(query)
        result = post.scalar()
        if not result:
            raise PostNotFoundException()
        return result

    async def create(
        self, session: AsyncSession, author_id: int, data: PostCreate
    ) -> Post:
        author = await session.get(self._author_model, author_id)
        if not author:
            raise UserNotFoundException()

        if data.category_id is not None:
            category = await session.get(
                self._category_model, data.category_id
            )
            if not category:
                raise CategoryNotFoundException()

        if data.location_id is not None:
            location = await session.get(
                self._location_model, data.location_id
            )
            if not location:
                raise LocationNotFoundException()

        post = self._model(author_id=author_id, **data.model_dump())
        session.add(post)
        await session.flush()
        return await self.get_by_id(session, post.id)

    async def update(
        self, session: AsyncSession, post_id: int, data: PostUpdate
    ) -> Post:
        post = await self.get_by_id(session, post_id)

        if (
            data.category_id is not None
            and data.category_id != post.category_id
        ):
            category = await session.get(
                self._category_model, data.category_id
            )
            if not category:
                raise CategoryNotFoundException()

        if (
            data.location_id is not None
            and data.location_id != post.location_id
        ):
            location = await session.get(
                self._location_model, data.location_id
            )
            if not location:
                raise LocationNotFoundException()

        update_data = data.model_dump(exclude_none=True)
        for key, value in update_data.items():
            setattr(post, key, value)
        await session.flush()
        return await self.get_by_id(session, post.id)

    async def delete(
        self, session: AsyncSession, post_id: int
    ) -> None:
        post = await self.get_by_id(session, post_id)
        await session.delete(post)
        await session.flush()
