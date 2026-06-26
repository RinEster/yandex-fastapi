from typing import List
from pathlib import Path
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile

from application.api.depends import (
    create_comment_use_case,
    delete_comment_use_case,
    get_comment_by_id_use_case,
    get_comments_by_post_use_case,
    update_comment_use_case,
    add_comment_image_use_case,
    get_comment_images_use_case,
    delete_all_comment_images_use_case,
    delete_single_comment_image_use_case,
)
from application.core.exceptions.domain_exception import (
    CommentNotFoundByIdException,
    PostNotFoundByIdException,
    UserNotFoundByIdException,
    NotCommentAuthorDomainException,
    CommentHasNoImageException,
    CommentHasNoImageIdException,
    UploadFileIsNotImageException,
)
from application.schemas.comments import (
    CommentCreate,
    CommentResponse,
    CommentUpdate,
    CommentImageResponse,
)
from application.schemas.users import UserResponse
from application.services.auth import AuthService

UPLOAD_DIR = Path("images/comments")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

comments_router = APIRouter()


@comments_router.get(
    "/post/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[CommentResponse],
)
async def get_comments_by_post(
    post_id: int, use_case=Depends(get_comments_by_post_use_case)
) -> List[CommentResponse]:
    try:
        return await use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@comments_router.get(
    "/id/{comment_id}",
    status_code=status.HTTP_200_OK,
    response_model=CommentResponse,
)
async def get_comment_by_id(
    comment_id: int, use_case=Depends(get_comment_by_id_use_case)
) -> CommentResponse:
    try:
        return await use_case.execute(comment_id=comment_id)
    except CommentNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@comments_router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentResponse,
)
async def create_comment(
    data: CommentCreate, use_case=Depends(create_comment_use_case),
    current_user: UserResponse = Depends(AuthService.get_current_user)
) -> CommentResponse:
    try:
        return await use_case.execute(data=data, author_id=current_user.id)
    except (
        PostNotFoundByIdException,
        UserNotFoundByIdException,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка при создании комментария: {str(e)}",
        )


@comments_router.put(
    "/update/{comment_id}",
    status_code=status.HTTP_200_OK,
    response_model=CommentResponse,
)
async def update_comment(
    comment_id: int,
    data: CommentUpdate,
    use_case=Depends(update_comment_use_case),
    current_user: UserResponse = Depends(AuthService.get_current_user)
) -> CommentResponse:
    try:
        return await use_case.execute(
            comment_id=comment_id, data=data, user_id=current_user.id
        )
    except CommentNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except NotCommentAuthorDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=e.get_detail()
        )


@comments_router.delete(
    "/id/{comment_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_comment(
    comment_id: int, 
    use_case=Depends(delete_comment_use_case),
    current_user: UserResponse = Depends(AuthService.get_current_user)
):
    try:
        await use_case.execute(comment_id=comment_id, user_id=current_user.id)
        return
    except CommentNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except NotCommentAuthorDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=e.get_detail()
        )


@comments_router.post(
    "/id/{comment_id}/images",
    status_code=status.HTTP_200_OK,
    response_model=CommentResponse,
)
async def add_comment_image(
    comment_id: int,
    file: UploadFile = File(...),
    use_case=Depends(add_comment_image_use_case),
    current_user: UserResponse = Depends(AuthService.get_current_user),
) -> CommentResponse:
    try:
        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = UPLOAD_DIR / filename

        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        return await use_case.execute(
            comment_id=comment_id,
            image_path=str(file_path),
            user_id=current_user.id
        )
    except CommentNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except UploadFileIsNotImageException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.get_detail()
        )
    except NotCommentAuthorDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=e.get_detail()
        )


@comments_router.get(
    "/id/{comment_id}/images",
    status_code=status.HTTP_200_OK,
    response_model=List[CommentImageResponse],
)
async def get_comment_images(
    comment_id: int,
    use_case=Depends(get_comment_images_use_case),
) -> List[CommentImageResponse]:
    try:
        return await use_case.execute(comment_id=comment_id)
    except (CommentNotFoundByIdException, CommentHasNoImageException) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@comments_router.delete(
    "/id/{comment_id}/images",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_all_comment_images(
    comment_id: int,
    use_case=Depends(delete_all_comment_images_use_case),
    current_user: UserResponse = Depends(AuthService.get_current_user),
):
    try:
        await use_case.execute(comment_id=comment_id, user_id=current_user.id)
    except CommentNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except NotCommentAuthorDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=e.get_detail()
        )


@comments_router.delete(
    "/id/{comment_id}/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_single_comment_image(
    comment_id: int,
    image_id: int,
    use_case=Depends(delete_single_comment_image_use_case),
    current_user: UserResponse = Depends(AuthService.get_current_user),
):
    try:
        await use_case.execute(
            comment_id=comment_id, image_id=image_id, user_id=current_user.id
        )
    except (CommentNotFoundByIdException, CommentHasNoImageIdException) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except NotCommentAuthorDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=e.get_detail()
        )
