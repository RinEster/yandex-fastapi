from typing import Type, List

from sqlalchemy.orm import Session, query

from infrastructure.sqlite.models.locations import Location


class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location

    def get(self, session: Session) -> List[Location]:
        query = session.query(self._model).all()
        return query 

