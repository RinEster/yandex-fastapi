from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import Location as LocationSchema

class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(
        self,
        name: str,
        is_published: bool = True
    ) -> LocationSchema:
        with self._database.session() as session:
            location = self._repo.create(
                session=session,
                name=name,
                is_published=is_published
            )

            location_data = {
                "id":location.id,
                "name":location.name,
                "is_published":location.is_published,
                "created_at":location.created_at
            }

            return LocationSchema.model_validate(obj=location_data)
