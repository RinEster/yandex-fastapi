from datetime import datetime
from typing import Type, List
from sqlalchemy.orm import Session
from infrastructure.sqlite.models.categories import Category
from core.exceptions.database_exceptions import(
    CategoryNotFoundException,
    CategorySlugAlreadyExistsException,
    CategoryTitleAlreadyExistsException
)
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
            raise CategoryNotFoundException
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
            raise CategoryNotFoundException
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
        title: str,
        description: str,
        slug: str,
        is_published: bool = True
    ) -> Category:
        if self.check_title_exists(session,title):
            raise CategoryTitleAlreadyExistsException
        
        if self.check_slug_exists(session,slug):
            raise CategorySlugAlreadyExistsException

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
         
        if title != category.title:
            if self.check_title_exists(session, title):
                raise CategoryTitleAlreadyExistsException
    
        if slug != category.slug:
            if self.check_slug_exists(session, slug):
                raise CategorySlugAlreadyExistsException

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
    )-> None:
        category = self.get_by_id(session,category_id)
        session.delete(category)
        session.flush()

