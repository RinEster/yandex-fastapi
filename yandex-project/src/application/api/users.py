from typing import List

from application.core.exceptions.domain_exception import (
    UserEmailIsNotUniqueException,
    UserLoginIsNotUniqueException,
    UserNotFoundByEmailException,
    UserNotFoundByIdException,
    UserNotFoundByLoginException,
)
from fastapi import APIRouter, Depends, HTTPException, status
from application.schemas.users import UserCreate, UserResponse
from application.services.auth import AuthService

from application.api.depends import (
    create_user_use_case,
    delete_user_use_case,
    get_all_users_use_case,
    get_user_by_email_use_case,
    get_user_by_id_use_case,
    get_user_by_login_use_case,
)

users_router = APIRouter()


@users_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[UserResponse],
)
async def get_all_users(
    use_case=Depends(get_all_users_use_case),
) -> List[UserResponse]:
    return await use_case.execute()


@users_router.get(
    "/id/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def get_user_by_id(
    user_id: int,
    user: UserResponse = Depends(AuthService.get_current_user),
    use_case=Depends(get_user_by_id_use_case),
) -> UserResponse:
    try:
        return await use_case.execute(user_id=user_id)
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )


@users_router.get(
    "/login/{login}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def get_user_by_login(
    login: str,
    user: UserResponse = Depends(AuthService.get_current_user),
    use_case=Depends(get_user_by_login_use_case),
) -> UserResponse:
    try:
        return await use_case.execute(login=login)
    except UserNotFoundByLoginException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )


@users_router.get(
    "/email/{email}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def get_user_by_email(
    email: str,
    user: UserResponse = Depends(AuthService.get_current_user),
    use_case=Depends(get_user_by_email_use_case),
) -> UserResponse:
    try:
        return await use_case.execute(email=email)
    except UserNotFoundByEmailException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )


@users_router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def create_user(
    data: UserCreate, use_case=Depends(create_user_use_case)
) -> UserResponse:
    try:
        return await use_case.execute(data=data)
    except UserLoginIsNotUniqueException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.get_detail(),
        )
    except UserEmailIsNotUniqueException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.get_detail(),
        )


@users_router.delete(
    "/id/{user_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
    user_id: int,
    user: UserResponse = Depends(AuthService.get_current_user),
    use_case=Depends(delete_user_use_case),
):
    try:
        await use_case.execute(user_id=user_id)
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
