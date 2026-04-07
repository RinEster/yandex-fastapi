from datetime import datetime
from typing import Type, List
from sqlalchemy.orm import Session
from sqlalchemy import insert
from datetime import datetime
from infrastructure.sqlite.models.categories import Category
from core.exceptions.database_exceptions import(
    CategoryNotFoundException,
    CategorySlugAlreadyExistsException,
    CategoryTitleAlreadyExistsException
)
from schemas.categories import CategoryCreate, CategoryUpdate

class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category


    def check_title_exists(
        self,
        session: Session,
        title: str
    )-> bool:
        query = (
            session.query(self._model)
            .where(self._model.title == title)
        )
        category = query.scalar()
        return category is not None

    def check_slug_exists(
        self,
        session: Session,
        slug: str,
    ) -> bool:
        query = (
            session.query(self._model)
            .where(self._model.slug == slug)
        )
        category = query.scalar()
        return category is not None

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
        category = query.scalar()
        if not category:
            raise CategoryNotFoundException()
        return category
    
    def get_by_slug(
        self,
        session: Session,
        slug: str
    ) -> Category:
        query = (
            session.query(self._model)
            .where(self._model.slug == slug)
        )
        category = query.scalar()
        if not category:
            raise CategoryNotFoundException()
        return category

    
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
        data: CategoryCreate
    ) -> Category:
        if self.check_title_exists(session, data.title):
            raise CategoryTitleAlreadyExistsException()
        
        if self.check_slug_exists(session, data.slug):
            raise CategorySlugAlreadyExistsException()
        
        if data.created_at is None:
            data.created_at = datetime.now()
        
        query = (
            insert(self._model)
            .values(data.model_dump(exclude_none=True))
            .returning(self._model)
        )
        
        category = session.scalar(query)
        session.flush()

        return category

    def update(
        self,
        session: Session,
        category_id: int,
        data: CategoryUpdate
    ) -> Category:
        category = self.get_by_id(session, category_id)
    
        if data.title is not None and data.title != category.title:
            if self.check_title_exists(session, data.title):
                raise CategoryTitleAlreadyExistsException()
            category.title = data.title

        if data.slug is not None and data.slug != category.slug:
            if self.check_slug_exists(session, data.slug):
                raise CategorySlugAlreadyExistsException()
            category.slug = data.slug
    
        if data.description is not None:
            category.description = data.description
    
        if data.is_published is not None:
            category.is_published = data.is_published
    
        session.flush()
        return category

    def delete(
        self,
        session: Session,
        category_id: int
    )-> None:
        category = self.get_by_id(session,category_id)
        session.delete(category)
        session.flush()

