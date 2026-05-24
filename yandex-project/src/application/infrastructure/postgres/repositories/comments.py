
from datetime import datetime
from typing import Type, List


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from application.schemas.comments import CommentBase, CommentCreate, CommentResponse, CommentUpdate
from application.infrastructure.postgres.models.comments import Comment
from application.infrastructure.postgres.models.posts import Post
from application.infrastructure.postgres.models.categories import Category
from application.infrastructure.postgres.models.locations import Location
from application.infrastructure.postgres.models.users import User
from application.core.exceptions.database_exceptions import(
    PostNotFoundException,
    UserNotFoundException,
    CommentNotFoundException
)


class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment
        self._post_model: Type[Post] = Post
        self._author_model: Type[User] = User

    async def get_all(
        self,
        session: AsyncSession 
    ) -> List[Comment]:
        query = select(self._model)
        result = await session.execute(query)
        return list(result.scalars().all())
    
    async def get_by_id(
        self,
        session: AsyncSession,
        comment_id: int
    ) -> Comment:
        query = (
            select(self._model)
            .where(self._model.id == comment_id)
        )
        comment = await session.scalar(query)
        if not comment:
            raise CommentNotFoundException()
        return comment

    async def get_by_post_id(
        self,
        session: AsyncSession,
        post_id: int
    ) -> List[Comment]:
        query = (
            select(self._model)
            .where(self._model.post_id == post_id)
            .order_by(self._model.created_at.desc())
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    async def get_by_author_id(
        self,
        session: AsyncSession,
        author_id: int
    ) -> List[Comment]:
        query = (
            select(self._model)
            .where(self._model.author_id == author_id)
            .order_by(self._model.created_at.desc())
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    async def create(
        self,
        session: AsyncSession,
        author_id: int,
        data: CommentCreate
    ) -> Comment:
        post = await session.get(self._post_model, data.post_id)
        if not post:
            raise PostNotFoundException()
        
        author = await session.get(self._author_model, author_id)
        if not author:
            raise UserNotFoundException()

        comment = self._model(
            post_id=data.post_id,
            author_id=author_id,
            text=data.text,
        )
        session.add(comment)
        await session.flush()
        return comment

    async def update(
        self,
        session: AsyncSession,
        comment_id: int,
        data: CommentUpdate
    ) -> Comment:
        comment = await self.get_by_id(session, comment_id)
       
        if data.text is not None:
            comment.text = data.text
        await session.flush()
        
        return comment

    async def delete(
        self,
        session: AsyncSession,
        comment_id: int
    ) -> None:
        comment = await self.get_by_id(session, comment_id)
        await session.delete(comment)
        await session.flush()

