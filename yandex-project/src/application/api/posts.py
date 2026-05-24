from typing import List
from application.services.auth import AuthService
from application.api.depends import (
    create_post_use_case,
    delete_post_use_case,
    get_all_posts_use_case,
    get_post_by_id_use_case,
    get_published_post_use_case,
    update_post_use_case,
)
from application.schemas.posts import (
    PostCreate,
    PostResponse,
    PostUpdate,
)
from application.schemas.users import UserResponse
from application.core.exceptions.domain_exception import (
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
    PostNotFoundByIdException,
    UserNotFoundByIdException,
)
from fastapi import APIRouter, Depends, HTTPException, status

posts_router = APIRouter()


@posts_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[PostResponse],
)
async def get_all_posts(
    use_case=Depends(get_all_posts_use_case),
) -> List[PostResponse]:
    return await use_case.execute()


@posts_router.get(
    "/id/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=PostResponse,
)
async def get_post_by_id(
    post_id: int, use_case=Depends(get_post_by_id_use_case)
) -> PostResponse:
    try:
        return await use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@posts_router.get(
    "/published",
    status_code=status.HTTP_200_OK,
    response_model=List[PostResponse],
)
async def get_published_posts(
    use_case=Depends(get_published_post_use_case),
) -> List[PostResponse]:
    return await use_case.execute()


@posts_router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    response_model=PostResponse,
)
async def create_post(
    data: PostCreate, use_case=Depends(create_post_use_case),
    current_user: UserResponse = Depends(AuthService.get_current_user)
) -> PostResponse:
    try:
        return await use_case.execute(data=data, author_id=current_user.id)
    except (
        CategoryNotFoundByIdException,
        LocationNotFoundByIdException,
        UserNotFoundByIdException,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка при создании поста: {str(e)}",
        )


@posts_router.put(
    "/id/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=PostResponse,
)
async def update_post(
    post_id: int,
    data: PostUpdate,
    use_case=Depends(update_post_use_case),
) -> PostResponse:
    try:
        return await use_case.execute(post_id=post_id, data=data)
    except (
        PostNotFoundByIdException,
        CategoryNotFoundByIdException,
        LocationNotFoundByIdException,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@posts_router.delete(
    "/id/{post_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_post(
    post_id: int, use_case=Depends(delete_post_use_case)
):
    try:
        await use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
