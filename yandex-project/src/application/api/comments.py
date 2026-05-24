from typing import List

from application.api.depends import (
    create_comment_use_case,
    delete_comment_use_case,
    get_comment_by_id_use_case,
    get_comments_by_post_use_case,
    update_comment_use_case,
)
from application.core.exceptions.domain_exception import (
    CommentNotFoundByIdException,
    PostNotFoundByIdException,
    UserNotFoundByIdException,
)
from application.schemas.comments import (
    CommentCreate,
    CommentResponse,
    CommentUpdate,
)
from fastapi import APIRouter, Depends, HTTPException, status

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
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
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
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@comments_router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentResponse,
)
async def create_comment(
    data: CommentCreate, use_case=Depends(create_comment_use_case)
) -> CommentResponse:
    try:
        return await use_case.execute(data=data)
    except (
        PostNotFoundByIdException,
        UserNotFoundByIdException,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
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
) -> CommentResponse:
    try:
        return await use_case.execute(
            comment_id=comment_id, data=data
        )
    except CommentNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@comments_router.delete(
    "/id/{comment_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_comment(
    comment_id: int, use_case=Depends(delete_comment_use_case)
):
    try:
        await use_case.execute(comment_id=comment_id)
        return
    except CommentNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
