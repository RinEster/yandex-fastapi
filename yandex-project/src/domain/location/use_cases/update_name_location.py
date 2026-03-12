from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import Location as LocationSchema

class UpdateLocationNameUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int, new_name: str) -> LocationSchema:
        with self._database.session() as session:
            location = self._repo.get_by_id(session, location_id)
            if not location:
                raise ValueError("Местоположение не найдено")
            
            updated = self._repo.update_name(session, location_id, new_name)
            session.commit()
           
            location_data = {
                "id":updated.id,
                "name":updated.name,
                "is_published":updated.is_published,
                "created_at":updated.created_at
            }

            return LocationSchema.model_validate(obj=location_data)
