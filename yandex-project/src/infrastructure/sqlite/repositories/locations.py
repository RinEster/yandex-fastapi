from datetime import datetime
from typing import Type, List
from sqlalchemy import insert
from sqlalchemy.orm import Session

from infrastructure.sqlite.models.locations import Location

from core.exceptions.database_exceptions import(
    LocationNameAlreadyExistsException,
    LocationNotFoundException
)

from schemas.locations import LocationCreate, LocationResponce, LocationUpdate

class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location
    
    def check_name_exists(
        self,
        session: Session,
        name: str
    )-> bool:
        query = (
            session.query(self._model)
            .where(self._model.name == name)
        )
        location = query.scalar()
        return location is not None

    def get_all(
            self,
            session: Session
    ) -> List[Location]:
        query = session.query(self._model).all()
        return query

    def get_by_id(
        self,
        session: Session,
        location_id: int
    ) -> Location:
        query = (
            session.query(self._model)
            .where(self._model.id == location_id)
        )
        location = query.scalar()
        if not location:
            raise LocationNotFoundException()
        return location

    def get_published(
        self,
        session: Session
    ) -> List[Location]:
        query =(
            session.query(self._model)
            .where(self._model.is_published == True).all()
        )
        return query

    def create(
        self, 
        session: Session,
        data: LocationCreate 
    ) -> Location:
        if self.check_name_exists(session, data.name):
            raise LocationNameAlreadyExistsException()

        if data.created_at is None:
            data.created_at = datetime.now()
        
        query = (
            session.insert(self._model)
            .values(data.model_dump(exclude_none=True))
            .returning(self._model)
        )

        location = session.scalar(query)
        session.flush()

        return location

    def update_name(
        self,
        session: Session,
        location_id: int,
        new_name: str
    ) -> Location:
        location = self.get_by_id(session,location_id)
        if location.name != new_name:
            if self.check_name_exists(session, new_name):
                raise LocationNameAlreadyExistsException()
        location.name=new_name
        session.flush()
        return location
        
    def delete(
        self,
        session: Session,
        location_id: int
    ) -> None:
        location = self.get_by_id(session, location_id)
        session.delete(location)
        session.flush()

