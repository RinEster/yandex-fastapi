import uuid
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile

from application.api.depends import (
    create_user_use_case,
    delete_user_use_case,
    get_all_users_use_case,
    get_user_by_email_use_case,
    get_user_by_id_use_case,
    get_user_by_login_use_case,
    update_user_use_case,
    upload_avatar_use_case,
    delete_avatar_use_case,
)
from application.core.exceptions.domain_exception import (
    UserEmailIsNotUniqueException,
    UserLoginIsNotUniqueException,
    UserNotFoundByEmailException,
    UserNotFoundByIdException,
    UserNotFoundByLoginException,
    UploadFileIsNotImageException,
)
from application.schemas.users import UserCreate, UserResponse, UserUpdate
from application.services.auth import AuthService

UPLOAD_DIR = Path("images/avatars")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

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


@users_router.put(
    "/id/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def update_user(
    user_id: int,
    data: UserUpdate,
    current_user: UserResponse = Depends(AuthService.get_current_user),
    use_case=Depends(update_user_use_case),
) -> UserResponse:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не можете редактировать чужой профиль",
        )

    try:
        return await use_case.execute(user_id=user_id, data=data)
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
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
    if user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не можете удалить чужой профиль",
        )

    try:
        await use_case.execute(user_id=user_id)
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )


@users_router.post(
    "/id/{user_id}/avatar",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def upload_user_avatar(
    user_id: int,
    file: UploadFile = File(...),
    current_user: UserResponse = Depends(AuthService.get_current_user),
    use_case=Depends(upload_avatar_use_case),
) -> UserResponse:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не можете изменить аватар другого пользователя",
        )

    try:
        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = UPLOAD_DIR / filename

        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        return await use_case.execute(user_id=user_id, image_path=str(file_path))
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except UploadFileIsNotImageException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.get_detail(),
        )


@users_router.delete(
    "/id/{user_id}/avatar",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def delete_user_avatar(
    user_id: int,
    current_user: UserResponse = Depends(AuthService.get_current_user),
    use_case=Depends(delete_avatar_use_case),
) -> UserResponse:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не можете удалить аватар другого пользователя",
        )

    try:
        return await use_case.execute(user_id=user_id)
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
