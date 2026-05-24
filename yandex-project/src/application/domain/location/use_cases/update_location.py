import logging

from application.core.exceptions.database_exceptions import (
    LocationNameAlreadyExistsException,
    LocationNotFoundException,
)
from application.core.exceptions.domain_exception import (
    LocationNameIsNotUniqueException,
    LocationNotFoundByIdException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.locations import (
    LocationRepository,
)
from application.schemas.locations import (
    LocationResponse,
    LocationUpdate,
)

logger = logging.getLogger(__name__)


class UpdateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(
        self, location_id: int, data: LocationUpdate
    ) -> LocationResponse:
        async with self._database.session() as session:
            try:
                location = await self._repo.update(
                    session=session,
                    location_id=location_id,
                    data=data,
                )
            except LocationNotFoundException:
                error = LocationNotFoundByIdException(id=location_id)
                logger.error(error.get_detail())
                raise error
            except LocationNameAlreadyExistsException:
                failed_name = data.name or "Указанное имя локации"
                error = LocationNameIsNotUniqueException(
                    name=failed_name
                )
                logger.error(error.get_detail())
                raise error

            return LocationResponse.model_validate(obj=location)
