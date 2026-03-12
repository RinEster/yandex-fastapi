
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository

class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> bool:
        with self._database.session() as session:
            location = self._repo.get_by_id(session, location_id)
            if not location:
                raise ValueError("Местоположение не найдено") 
            result = self._repo.delete_location(session, location_id)
            return result
