from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import LocationResponce, LocationCreate
from src.core.exceptions.database_exceptions import LocationNameAlreadyExistsException


from src.core.exceptions.domain_exception import LocationTitleIsNotUniqueException

import logging

logger = logging.getLogger(__name__)

class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(
        self,
        data: LocationCreate
    ) -> LocationResponce:
        with self._database.session() as session:
            try:
                location = self._repo.create(session=session, data=data)
            except LocationNameAlreadyExistsException:
                error = LocationTitleIsNotUniqueException(name=data.name)
                logger.error(error.get_detail())
                raise error

            return LocationResponce.model_validate(obj=location)
