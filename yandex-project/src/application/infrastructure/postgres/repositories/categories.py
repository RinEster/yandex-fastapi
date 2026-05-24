from datetime import datetime
from typing import List, Type

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    CategorySlugAlreadyExistsException,
    CategoryTitleAlreadyExistsException,
)
from application.infrastructure.postgres.models.categories import Category
from application.schemas.categories import CategoryCreate, CategoryUpdate
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession


class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    async def check_title_exists(self, session: AsyncSession, title: str) -> bool:
        query = select(self._model).where(self._model.title == title)
        category = await session.scalar(query)
        return category is not None

    async def check_slug_exists(
        self,
        session: AsyncSession,
        slug: str,
    ) -> bool:
        query = select(self._model).where(self._model.slug == slug)
        category = await session.scalar(query)
        return category is not None

    async def get_all(self, session: AsyncSession) -> List[Category]:
        query = select(self._model)
        result = await session.execute(query)
        categories = result.scalars().all()
        return list(categories)

    async def get_by_id(self, session: AsyncSession, category_id: int) -> Category:
        query = select(self._model).where(self._model.id == category_id)
        category = await session.scalar(query)
        if not category:
            raise CategoryNotFoundException()
        return category

    async def get_by_slug(self, session: AsyncSession, slug: str) -> Category:
        query = select(self._model).where(self._model.slug == slug)
        category = await session.scalar(query)
        if not category:
            raise CategoryNotFoundException()
        return category

    async def get_published(self, session: AsyncSession) -> List[Category]:
        query = (
            select(self._model)
            .where(self._model.is_published.is_(True))
        )
        result = await session.execute(query)
        published_categories = result.scalars().all()
        return list(published_categories)

    async def create(self, session: AsyncSession, data: CategoryCreate) -> Category:
        if await self.check_title_exists(session, data.title):
            raise CategoryTitleAlreadyExistsException()

        if await self.check_slug_exists(session, data.slug):
            raise CategorySlugAlreadyExistsException()

        if data.created_at is None:
            data.created_at = datetime.now()

        query = (
            insert(self._model)
            .values(data.model_dump(exclude_none=True))
            .returning(self._model)
        )

        result = await session.execute(query)
        category = result.scalar_one()
        
        await session.flush()

        return category

    async def update(
        self, session: AsyncSession, category_id: int, data: CategoryUpdate
    ) -> Category:
        category = await self.get_by_id(session, category_id)

        if data.title is not None and data.title != category.title:
            if await self.check_title_exists(session, data.title):
                raise CategoryTitleAlreadyExistsException()
            category.title = data.title

        if data.slug is not None and data.slug != category.slug:
            if await self.check_slug_exists(session, data.slug):
                raise CategorySlugAlreadyExistsException()
            category.slug = data.slug

        if data.description is not None:
            category.description = data.description

        if data.is_published is not None:
            category.is_published = data.is_published

        await session.flush()
        return category

    async def delete(self, session: AsyncSession, category_id: int) -> None:
        category = self.get_by_id(session, category_id)
        await session.delete(category)
        await session.flush()
