from datetime import datetime
from typing import Type, List
from sqlalchemy.orm import Session
from infrastructure.sqlite.models.categories import Category

class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    def get_all(
        self,
        session: Session
    ) -> List[Category]:
        query = session.query(self._model).all()
        return query

    def get_by_id(
        self,
        session: Session,
        category_id: int
    ) -> Category:
        query = (
            session.query(self._model)
            .where(self._model.id == category_id)
        )
        return query.scalar()

    def get_published(
        self,
        session: Session
    ) -> List[Category]:
        query = (
            session.query(self._model)
            .where(self._model.is_published == True).all()
        )
        return query

    def create(
        self,
        session: Session,
        title: str,
        description: str,
        slug: str,
        is_published: bool = True
    ) -> Category:
        category = self._model(
            title=title,
            description=description,
            slug=slug,
            is_published=is_published,
            created_at=datetime.now()
        )
        session.add(category)
        session.flush()
        return category

    def update(
        self,
        session: Session,
        category_id: int,
        title:str,
        description: str,
        slug: str,
        is_published: bool = True
    ) -> Category:
        category = self.get_by_id(session,category_id)
        if category:
            category.title=title
            category.description=description
            category.slug=slug
            category.is_published=is_published
            session.flush()
        return category

    def delete(
        self,
        session: Session,
        category_id: int
    )-> bool:
        category = self.get_by_id(session,category_id)
        if category:
            session.delete(category)
            session.flush()
            return True
        return False


