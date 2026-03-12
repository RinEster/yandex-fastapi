from typing import List
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository
from schemas.posts import Post as PostSchema

class GetAllPostsUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self) -> List[PostSchema]:
        with self._database.session() as session:
            posts = self._repo.get_all(session)
            
            result = []
            for post in posts:
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
                result.append(PostSchema.model_validate(obj=post_dict))
            
            return result
