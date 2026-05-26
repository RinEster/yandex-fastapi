from typing import List, Type

from application.core.exceptions.database_exceptions import (
    LocationNameAlreadyExistsException,
    LocationNotFoundException,
)
from application.infrastructure.postgres.models.locations import (
    Location,
)
from application.schemas.locations import (
    LocationCreate,
    LocationUpdate,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.exc import IntegrityError

class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location

    async def check_name_exists(
        self, session: AsyncSession, name: str
    ) -> bool:
        query = select(self._model).where(self._model.name == name)
        result = await session.execute(query)
        location = result.scalar_one_or_none()
        return location is not None

    async def get_all(self, session: AsyncSession) -> List[Location]:
        query = select(self._model)
        result = await session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(
        self, session: AsyncSession, location_id: int
    ) -> Location:
        query = select(self._model).where(
            self._model.id == location_id
        )
        result = await session.execute(query)
        location = result.scalar_one_or_none()
        if not location:
            raise LocationNotFoundException()
        return location

    async def get_published(
        self, session: AsyncSession
    ) -> List[Location]:
        query = select(self._model).where(
            self._model.is_published.is_(True)
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    async def create(
        self, session: AsyncSession, data: LocationCreate
    ) -> Location:

        location = self._model(**data.model_dump())
        session.add(location)
        try:
            await session.flush()
        except IntegrityError:
            await session.rollback()
            raise LocationNameAlreadyExistsException()
        return location

    async def update(
        self,
        session: AsyncSession,
        location_id: int,
        data: LocationUpdate,
    ) -> Location:
        location = await self.get_by_id(session, location_id)

        update_data = data.model_dump(exclude_none=True)
        for key, value in update_data.items():
            setattr(location, key, value)
        try:
            await session.flush()
        except IntegrityError:
            await session.rollback()
            raise LocationNameAlreadyExistsException()
        return location

    async def delete(
        self, session: AsyncSession, location_id: int
    ) -> None:
        location = await self.get_by_id(session, location_id)
        await session.delete(location)
        await session.flush()
