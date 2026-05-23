from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository
from schemas.posts import Post as PostSchema

class UpdatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self,
        post_id: int,
        title: str,
        text: str,
        location_id: int,
        category_id: int,
        image: str,
        is_published: bool
    ) -> PostSchema:
        with self._database.session() as session:
            post = self._repo.get_by_id(session, post_id)
            if not post:
                raise ValueError("Пост не найден")
            
            updated = self._repo.update(
                session=session,
                post_id=post_id,
                title=title,
                text=text,
                location_id=location_id,
                category_id=category_id,
                image=image,
                is_published=is_published
            )
            
            post_dict = {
                "id": updated.id,
                "title": updated.title,
                "text": updated.text,
                "pub_date": updated.pub_date,
                "author_id": updated.author_id,
                "location_id": updated.location_id,
                "category_id": updated.category_id,
                "image": updated.image,
                "is_published": updated.is_published,
                "created_at": updated.created_at
            }
            
            return PostSchema.model_validate(obj=post_dict)
