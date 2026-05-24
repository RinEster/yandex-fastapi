import logging

from application.core.exceptions.database_exceptions import (
    LocationNotFoundException,
)
from application.core.exceptions.domain_exception import (
    LocationNotFoundByIdException,
)
from application.infrastructure.postgres.database import database
from application.infrastructure.postgres.repositories.locations import (
    LocationRepository,
)

logger = logging.getLogger(__name__)


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> None:
        async with self._database.session() as session:
            try:
                await self._repo.delete(
                    session=session, location_id=location_id
                )
            except LocationNotFoundException:
                error = LocationNotFoundByIdException(id=location_id)
                logger.error(error.get_detail())
                raise error
