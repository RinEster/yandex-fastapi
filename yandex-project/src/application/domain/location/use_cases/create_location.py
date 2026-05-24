import logging

from application.core.exceptions.database_exceptions import (
    LocationNameAlreadyExistsException,
)
from application.core.exceptions.domain_exception import (
    LocationNameIsNotUniqueException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.locations import (
    LocationRepository,
)
from application.schemas.locations import (
    LocationCreate,
    LocationResponse,
)

logger = logging.getLogger(__name__)


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, data: LocationCreate) -> LocationResponse:
        async with self._database.session() as session:
            try:
                location = await self._repo.create(
                    session=session, data=data
                )
            except LocationNameAlreadyExistsException:
                error = LocationNameIsNotUniqueException(
                    name=data.name
                )
                logger.error(error.get_detail())
                raise error

            return LocationResponse.model_validate(obj=location)
