from typing import List

from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.locations import (
    LocationRepository,
)
from application.schemas.locations import LocationResponse


class GetAllLocationsUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self) -> List[LocationResponse]:
        async with self._database.session() as session:
            locations = await self._repo.get_all(session)
            return [
                LocationResponse.model_validate(obj=loc)
                for loc in locations
            ]
