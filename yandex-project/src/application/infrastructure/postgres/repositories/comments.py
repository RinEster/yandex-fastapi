from typing import List, Type
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.exceptions.database_exceptions import (
    CommentNotFoundException,
    PostNotFoundException,
    UserNotFoundException,
    NotCommentAuthor,
    CommentImageNotFoundException,
)
from application.infrastructure.postgres.models.comments import (
    Comment, CommentImage
)
from application.infrastructure.postgres.models.posts import Post
from application.infrastructure.postgres.models.users import User
from application.schemas.comments import (
    CommentCreate,
    CommentUpdate,
)

class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment
        self._post_model: Type[Post] = Post
        self._author_model: Type[User] = User
        self._comment_image_model: Type[CommentImage] = CommentImage 

    def _get_base_query(self):
        return select(self._model).options(
            selectinload(self._model.images)
        )

    async def get_all(self, session: AsyncSession) -> List[Comment]:
        query = self._get_base_query()
        result = await session.execute(query)
        return list(result.unique().scalars().all())

    async def get_by_id(
        self, session: AsyncSession, comment_id: int
    ) -> Comment:
        query = self._get_base_query().where(
            self._model.id == comment_id
        )
        result = await session.execute(query)
        comment = result.unique().scalar_one_or_none()
        if not comment:
            raise CommentNotFoundException()
        return comment

    async def get_by_post_id(
        self, session: AsyncSession, post_id: int
    ) -> List[Comment]:
        query = (
            self._get_base_query()
            .where(self._model.post_id == post_id)
            .order_by(self._model.created_at.desc())
        )
        result = await session.execute(query)
        return list(result.unique().scalars().all())

    async def get_by_author_id(
        self, session: AsyncSession, author_id: int
    ) -> List[Comment]:
        query = (
            self._get_base_query()
            .where(self._model.author_id == author_id)
            .order_by(self._model.created_at.desc())
        )
        result = await session.execute(query)
        return list(result.unique().scalars().all())

    async def create(
        self,
        session: AsyncSession,
        author_id: int,
        data: CommentCreate,
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
        
        if data.images:
            for img in data.images:
                comment.images.append(
                    self._comment_image_model(image_url=img.image_url)
                )

        session.add(comment)
        await session.flush()
        
        return comment

    async def update(
        self,
        session: AsyncSession,
        comment_id: int,
        data: CommentUpdate,
        user_id: int,
    ) -> Comment:
        comment = await self.get_by_id(session, comment_id)

        if comment.author_id != user_id:
            raise NotCommentAuthor()

        if data.text is not None:
            comment.text = data.text
            
        await session.flush()
        return comment

    async def delete(
        self, session: AsyncSession, comment_id: int, user_id: int
    ) -> None:
        comment = await self.get_by_id(session, comment_id)

        if comment.author_id != user_id:
            raise NotCommentAuthor()

        await session.delete(comment)
        await session.flush()
    async def add_comment_image(
        self,
        session: AsyncSession,
        comment_id: int,
        image_url: str,
        user_id: int
    ) -> Comment:
        comment = await self.get_by_id(session, comment_id)

        if comment.author_id != user_id:
            raise NotCommentAuthor()

        comment.images.append(self._comment_image_model(image_url=image_url))

        await session.flush()
        return comment

    async def get_comment_images(
        self, session: AsyncSession, comment_id: int
    ) -> List[CommentImage]:
        comment = await self.get_by_id(session, comment_id)
        return comment.images

    async def delete_single_image(
        self,
        session: AsyncSession,
        comment_id: int,
        image_id: int,
        user_id: int
    ) -> None:
        comment = await self.get_by_id(session, comment_id)

        if comment.author_id != user_id:
            raise NotCommentAuthor()

        target_image = None
        for img in comment.images:
            if img.id == image_id:
                target_image = img
                break

        if not target_image:
            raise CommentImageNotFoundException()

        await session.delete(target_image)
        await session.flush()

    async def delete_all_images(
        self,
        session: AsyncSession,
        comment_id: int,
        user_id: int
    ) -> None:
        comment = await self.get_by_id(session, comment_id)

        if comment.author_id != user_id:
            raise NotCommentAuthor()

        comment.images.clear()
        
        await session.flush()
