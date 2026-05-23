from datetime import datetime
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.posts import Post as PostSchema

class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()

    async def execute(
        self,
        title: str,
        text: str,
        pub_date: datetime,
        author_id: int,
        location_id: int | None = None,
        category_id: int | None = None,
        image: str | None = None,
        is_published: bool = True
    ) -> PostSchema:
        with self._database.session() as session:
            author = self._user_repo.get_user_by_id(session, author_id)
            if not author:
                raise ValueError("Автор не найден")
            
            post = self._repo.create(
                session=session,
                title=title,
                text=text,
                pub_date=pub_date,
                author_id=author_id,
                location_id=location_id,
                category_id=category_id,
                image=image,
                is_published=is_published
            )
            
            post_dict = {
                "id": post.id,
                "title": post.title,
                "text": post.text,
                "pub_date": post.pub_date,
                "author_id": post.author_id,
                "location_id": post.location_id,
                "category_id": post.category_id,
                "image": post.image,
                "is_published": post.is_published,
                "created_at": post.created_at
            }
            
            return PostSchema.model_validate(obj=post_dict)
