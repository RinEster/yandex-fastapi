from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import LocationResponce, LocationUpdate

from core.exceptions.database_exceptions import(
    LocationNotFoundException,
    LocationNameAlreadyExistsException
)

from core.exceptions.domain_exception import(
    LocationNotFoundByIdException,
    LocationTitleIsNotUniqueException
)

import logging

logger = logging.getLogger(__name__)

class UpdateLocationNameUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self,
                      location_id: int, 
                      data: LocationUpdate
    ) -> LocationResponce:
        with self._database.session() as session:
            try:
                location = self._repo.update(
                session=session,
                location_id=location_id,
                data=data
            )
            except LocationNotFoundException:
                error = LocationNotFoundByIdException(id=location_id)
                logger.error(error.get_detail())
                raise error

            return LocationResponce.model_validate(obj=location)
