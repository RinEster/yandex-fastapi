from typing import List

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import LocationResponce

class GetAllLocationsUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self) -> List[LocationResponce]:
        with self._database.session() as session:
            locations = self._repo.get_all(session)
            
            result = []
            for location in locations:
                result.append(LocationResponce.model_validate(obj=location))
            
            return result

