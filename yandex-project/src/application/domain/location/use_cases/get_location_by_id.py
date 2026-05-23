from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import LocationResponce

from core.exceptions.database_exceptions import LocationNotFoundException

from core.exceptions.domain_exception import LocationNotFoundByIdException

import logging

logger = logging.getLogger(__name__)

class GetLocationByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> LocationResponce:
        with self._database.session() as session:
            try:
               location = self._repo.get_by_id(session, location_id)
            except LocationNotFoundException:
                error = LocationNotFoundByIdException(id=location_id)
                logger.error(error.get_detail())
                raise error
            return LocationResponce.model_validate(obj=location)
