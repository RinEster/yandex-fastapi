from datetime import datetime
from typing import Type, List

from sqlalchemy.orm import Session

from infrastructure.sqlite.models.locations import Location


class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location

    def get_all(self, session: Session) -> List[Location]:
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
        return query.scalar()

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
        name: str, 
        is_published: bool = True
    ) -> Location:
        location = self._model(
            name=name,
            is_published=is_published,
            created_at=datetime.now()
        )
        session.add(location)
        session.commit()
        return location

    def update_name(
        self,
        session: Session,
        location_id: int,
        new_name: str
    ) -> Location:
        location = self.get_by_id(session,location_id)
        if location:
            location.name=new_name
            session.commit()
        return location
        
    def delete_location(
        self,
        session: Session,
        location_id: int
    ) -> bool:
        location = self.get_by_id(session, location_id)
        if location:
            session.delete(location)
            session.commit()
            return True
        return False


