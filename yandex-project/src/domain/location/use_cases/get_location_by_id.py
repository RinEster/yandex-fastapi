from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.location import Location as LocationSchema

class GetLocationByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> LocationSchema:
        with self._database.session() as session:
            location = self._repo.get_by_id(session, location_id)
            
            if not location:
                raise ValueError("Местоположение не найдено")
           
            location_dict = {
                "id": location.id,
                "name": location.name,
                "is_published": location.is_published,
                "created_at": location.created_at
            }
            
            return LocationSchema.model_validate(obj=location_dict)
