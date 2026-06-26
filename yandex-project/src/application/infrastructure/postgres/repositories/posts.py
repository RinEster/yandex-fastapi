from typing import List, Type, Dict, Any

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    LocationNotFoundException,
    PostNotFoundException,
    UserNotFoundException,
    PostImageNotFoundException,
    NotPostAuthorException,
)
from application.infrastructure.postgres.models.categories import (
    Category,
)
from application.infrastructure.postgres.models.locations import (
    Location,
)
from application.infrastructure.postgres.models.posts import Post, PostImage
from application.infrastructure.postgres.models.users import User
from application.schemas.posts import PostCreate, PostUpdate
from sqlalchemy import Select, select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post
        self._image_model: Type[PostImage] = PostImage
        self._author_model: Type[User] = User
        self._location_model: Type[Location] = Location
        self._category_model: Type[Category] = Category

    def _get_base_query(self) -> Select:
        return select(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.category),
            joinedload(self._model.location),
            selectinload(self._model.comments),
            selectinload(self._model.images),
        )

    def _build_pagination_response(
        self,
        items: List[Post],
        total: int,
        page: int,
        size: int
    ) -> dict:
        pages = (total + size - 1) // size if total > 0 else 0
        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "pages": pages,
            "has_next": page < pages,
            "has_prev": page > 1,
        }

    async def get_all(
        self,
        session: AsyncSession,
        page: int = 1,
        size: int = 10
    ) -> dict:
        count_ch = select(func.count(self._model.id))
        count_res = await session.execute(count_ch)
        total = count_res.scalar() or 0

        offset_value = (page - 1) * size
        query = self._get_base_query().limit(size).offset(offset_value)
        result = await session.execute(query)
        items = list(result.scalars().all())
        return self._build_pagination_response(items, total, page, size)

    async def get_published(
        self, 
        session: AsyncSession,
        page: int = 1,
        size: int = 15
    ) -> dict:
        count_ch = select(func.count(self._model.id)).where(
            self._model.is_published.is_(True)
        )
        count_res = await session.execute(count_ch)
        total = count_res.scalar() or 0

        offset_value = (page - 1) * size
        query = (
            self._get_base_query()
            .where(self._model.is_published.is_(True))
            .order_by(self._model.pub_date.desc())
            .limit(size)
            .offset(offset_value)
        )
        result = await session.execute(query)
        items = list(result.scalars().all())
        return self._build_pagination_response(items, total, page, size)


    async def get_by_id(
        self, session: AsyncSession, post_id: int
    ) -> Post:
        query = self._get_base_query().where(
            self._model.id == post_id
        )
        post = await session.execute(query)
        result = post.scalar()
        if not result:
            raise PostNotFoundException()
        return result

    async def create(
        self, session: AsyncSession, author_id: int, data: PostCreate
    ) -> Post:
        author = await session.get(self._author_model, author_id)
        if not author:
            raise UserNotFoundException()

        if data.category_id is not None:
            category = await session.get(
                self._category_model, data.category_id
            )
            if not category:
                raise CategoryNotFoundException()

        if data.location_id is not None:
            location = await session.get(
                self._location_model, data.location_id
            )
            if not location:
                raise LocationNotFoundException()
        
        images_data = getattr(data, "images", None) or []
        post_data = data.model_dump(exclude={"images"}) if hasattr(data,"images") else data.model_dump()
        post = self._model(author_id=author_id, **post_data)

        for img_url in images_data:
            post.images.append(self._image_model(image_url=img_url))
        session.add(post)
        await session.flush()
        return await self.get_by_id(session, post.id)

    async def update(
        self,
        session: AsyncSession,
        post_id: int,
        data: PostUpdate,
        user_id: int
    ) -> Post:
        post = await self.get_by_id(session, post_id)

        if post.author_id != user_id:
            raise NotPostAuthorException()

        if (
            data.category_id is not None
            and data.category_id != post.category_id
        ):
            category = await session.get(
                self._category_model, data.category_id
            )
            if not category:
                raise CategoryNotFoundException()

        if (
            data.location_id is not None
            and data.location_id != post.location_id
        ):
            location = await session.get(
                self._location_model, data.location_id
            )
            if not location:
                raise LocationNotFoundException()

        if hasattr(data, "images") and data.images is not None:
            post.images.clear()
            for img_url in data.images:
                post.images.append(self._image_model(image_url=img_url))

        update_data = data.model_dump(exclude_none=True, exclude={"images","user_id"})
        for key, value in update_data.items():
            setattr(post, key, value)
        await session.flush()
        return await self.get_by_id(session, post.id)

    async def delete(
        self,
        session: AsyncSession,
        post_id: int,
        user_id: int
    ) -> None:
        post = await self.get_by_id(session, post_id)

        if post.author_id != user_id:
            raise NotPostAuthorException()

        await session.delete(post)
        await session.flush()


    async def add_post_images(
        self,
        session: AsyncSession,
        post_id: int,
        image_urls: List[str],
        user_id: int
    ) -> Post:

        post = await self.get_by_id(session, post_id)

        if post.author_id != user_id:
            raise NotPostAuthorException()

        for url in image_urls:
            post.images.append(self._image_model(image_url=url))


        await session.flush()
        return post

    async def get_post_images(
        self, session: AsyncSession, post_id: int
    ) -> List[PostImage]:
        post = await self.get_by_id(session, post_id)
        return post.images

    async def delete_single_image(
        self,
        session: AsyncSession,
        post_id: int,
        image_id: int,
        user_id: int
    ) -> None:
        post = await self.get_by_id(session, post_id)

        if post.author_id != user_id:
            raise NotPostAuthorException()

        target_image = None
        for img in post.images:
            if img.id == image_id:
                target_image = img
                break

        if not target_image:
            raise PostImageNotFoundException()

        await session.delete(target_image)
        await session.flush()

    async def delete_all_images(
        self,
        session: AsyncSession,
        post_id: int,
        user_id: int
    )-> None:
        post = await self.get_by_id(session, post_id)

        if post.author_id != user_id:
            raise NotPostAuthorException()

        post.images.clear()
        await session.flush()
        

    async def update_post_images(
        self,
        session: AsyncSession,
        post_id:int,
        user_id: int,
        image_urls: List[str]
    ) -> Post:
        post = await self.get_by_id(session, post_id)
        if post.author_id != user_id:
            raise NotPostAuthorException()
        post.images.clear()
        for url in image_urls:
            post.images.append(self._image_model(image_url=url))

        await session.flush()
        return post

