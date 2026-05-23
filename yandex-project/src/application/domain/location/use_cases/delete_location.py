
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from core.exceptions.database_exceptions import LocationNotFoundException
from core.exceptions.domain_exception import LocationNotFoundByIdException
import logging

logger = logging.getLogger(__name__)

class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> None:
        with self._database.session() as session:
            try:
                self._repo.delete(session=session, location_id=location_id)
            except LocationNotFoundException:
                error = LocationNotFoundByIdException(id=location_id)
                logger.error(error.get_detail())
                raise error
