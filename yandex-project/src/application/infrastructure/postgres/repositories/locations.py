from datetime import datetime, UTC
from typing import Type, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.postgres.models.locations import Location

from core.exceptions.database_exceptions import(
    LocationNameAlreadyExistsException,
    LocationNotFoundException
)

from schemas.locations import LocationCreate, LocationUpdate

class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location
    
    async def check_name_exists(
        self,
        session: AsyncSession,
        name: str
    )-> bool:
        query = (
            select(self._model)
            .where(self._model.name == name)
        )
        result = await session.execute(query)
        location = result.scalar_one_or_none()
        return location is not None

    async def get_all(
            self,
            session: AsyncSession
    ) -> List[Location]:
        query = select(self._model)
        result = await session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(
        self,
        session: AsyncSession,
        location_id: int
    ) -> Location:
        query = (
            select(self._model)
            .where(self._model.id == location_id)
        )
        result = await session.execute(query)
        location = result.scalar_one_or_none()
        if not location:
            raise LocationNotFoundException()
        return location

    async def get_published(
        self,
        session: AsyncSession
    ) -> List[Location]:
        query =(
            select(self._model)
            .where(self._model.is_published.is_(True))
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    async def create(
        self, 
        session: AsyncSession,
        data: LocationCreate 
    ) -> Location:
        if await self.check_name_exists(session, data.name):
            raise LocationNameAlreadyExistsException()

        values = data.model_dump(exclude_none=True)

        if "created_at" not in values:
            values["created_at"] = datetime.now(UTC)
        
        location = self._model(**values)
        session.add(location)
        await session.flush()

        return location

    async def update(
        self,
        session: AsyncSession,
        location_id: int,
        data: LocationUpdate
    ) -> Location:
        location = await self.get_by_id(session, location_id)
    
        if data.name is not None and location.name != data.name:
                if await self.check_name_exists(session, data.name):
                    raise LocationNameAlreadyExistsException()
                location.name = data.name
    
        if data.is_published is not None:
            location.is_published = data.is_published
    
        if data.created_at is not None:
            location.created_at = data.created_at
    
        await session.flush()
        return location        
    

    async def delete(
        self,
        session: AsyncSession,
        location_id: int
    ) -> None:
        location = await self.get_by_id(session, location_id)
        await session.delete(location)
        await session.flush()

