from typing import List, Annotated
from application.services.auth import AuthService
from application.api.depends import (
    create_post_use_case, 
    delete_post_use_case,
    get_all_posts_use_case,
    get_post_by_id_use_case,
    get_published_post_use_case,
    update_post_use_case,
    get_post_images_use_case,
    add_post_images_use_case,
    delete_all_images_use_case,
    delete_single_image_use_case,
    get_post_by_category_use_case,
)
from application.schemas.posts import (
    PostCreate,
    PostResponse,
    PostUpdate,
    PostImageResponse
)
from application.schemas.users import UserResponse
from application.core.exceptions.domain_exception import (
    NotPostAuthorDomainException,
    PostHasNoImageIdException,
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
    PostNotFoundByIdException,
    UserNotFoundByIdException,
    PostHasNoImageException,
    UploadFileIsNotImageException
)

from application.schemas.page import Page
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from pathlib import Path
import uuid

UPLOAD_DIR = Path("images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
posts_router = APIRouter()

@posts_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Page[PostResponse],
)
async def get_all_posts(
    page: int = 1,
    size: int = 15,
    use_case=Depends(get_all_posts_use_case),
) -> Page[PostResponse]:
    return await use_case.execute(page=page, size=size)


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
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@posts_router.get(
    "/published",
    status_code=status.HTTP_200_OK,
    response_model=Page[PostResponse],
)
async def get_published_posts(
    page: int = 1,
    size: int = 15,
    use_case=Depends(get_published_post_use_case),
) -> Page[PostResponse]:
    return await use_case.execute(page=page, size=size)

@posts_router.get(
    "/category/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=Page[PostResponse],
)
async def get_posts_by_category(
    category_id: int,
    page: int = 1,
    size: int = 15,
    use_case=Depends(get_post_by_category_use_case)
) -> Page[PostResponse]:
    try:
        return await use_case.execute(category_id=category_id,page=page,size=size)
    except  CategoryNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )

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
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
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
    current_user: UserResponse = Depends(AuthService.get_current_user)
) -> PostResponse:
    try:
        return await use_case.execute(post_id=post_id, data=data, user_id=current_user.id)
    except (
        PostNotFoundByIdException,
        CategoryNotFoundByIdException,
        LocationNotFoundByIdException,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except NotPostAuthorDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=e.get_detail()
        )


@posts_router.delete(
    "/id/{post_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_post(
    post_id: int, use_case=Depends(delete_post_use_case),
    current_user: UserResponse = Depends(AuthService.get_current_user)
):
    try:
        await use_case.execute(post_id=post_id, user_id=current_user.id)
    except PostNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except NotPostAuthorDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=e.get_detail()
        )


@posts_router.post(
    "/id/{post_id}/images",
    status_code=status.HTTP_200_OK,
    response_model=PostResponse,
)
async def add_post_images(
    post_id: int,
    file: UploadFile = File(...),
    use_case=Depends(add_post_images_use_case),
    current_user: UserResponse = Depends(AuthService.get_current_user),
) -> PostResponse:
    try:
        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = UPLOAD_DIR / filename

        content = await file.read()

        with open(file_path, "wb") as f:
            f.write(content)

        return await use_case.execute(
            post_id=post_id,
            image_path=str(file_path),
            user_id=current_user.id
        )
    except PostNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except UploadFileIsNotImageException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.get_detail()
        )
    except NotPostAuthorDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=e.get_detail()
        )


@posts_router.get(
    "/id/{post_id}/images",
    status_code=status.HTTP_200_OK,
    response_model=List[PostImageResponse],
)
async def get_post_images(
    post_id: int,
    use_case=Depends(get_post_images_use_case),
) -> List[PostImageResponse]:
    try:
        return await use_case.execute(post_id=post_id)
    except (PostNotFoundByIdException, PostHasNoImageException) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@posts_router.delete(
    "/id/{post_id}/images",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_all_post_images(
    post_id: int,
    use_case=Depends(delete_all_images_use_case),
    current_user: UserResponse = Depends(AuthService.get_current_user),
):
    try:
        await use_case.execute(post_id=post_id, user_id=current_user.id)
    except PostNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except NotPostAuthorDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=e.get_detail()
        )


@posts_router.delete(
    "/id/{post_id}/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_single_post_image(
    post_id: int,
    image_id: int,
    use_case=Depends(delete_single_image_use_case),
    current_user: UserResponse = Depends(AuthService.get_current_user),
):
    try:
        await use_case.execute(post_id=post_id, image_id=image_id, user_id=current_user.id)
    except (PostNotFoundByIdException, PostHasNoImageIdException) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except NotPostAuthorDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=e.get_detail()
        )
