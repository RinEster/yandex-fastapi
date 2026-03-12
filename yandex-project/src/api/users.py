from fastapi import APIRouter, status, HTTPException, Depends
from typing import List

from schemas.users import User  

from api.depends import (
    get_create_user_use_case,
    get_get_user_by_id_use_case,
    get_get_user_by_login_use_case,
    get_get_user_by_email_use_case,
    get_get_all_users_use_case,
    get_update_user_login_use_case,
    get_update_user_email_use_case,
    get_update_user_password_use_case,
    get_update_user_name_use_case,
    get_delete_user_use_case
)

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[User])
async def get_all_users(
    use_case = Depends(get_get_all_users_use_case)
) -> List[User]:
    users = await use_case.execute()
    return users


@router.get("/id/{user_id}", status_code=status.HTTP_200_OK, response_model=User)
async def get_user_by_id(
    user_id: int,
    use_case = Depends(get_get_user_by_id_use_case)
) -> User:
    try:
        user = await use_case.execute(user_id=user_id)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/login/{login}", status_code=status.HTTP_200_OK, response_model=User)
async def get_user_by_login(
    login: str,
    use_case = Depends(get_get_user_by_login_use_case)
) -> User:
    try:
        user = await use_case.execute(login=login)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/email/{email}", status_code=status.HTTP_200_OK, response_model=User)
async def get_user_by_email(
    email: str,
    use_case = Depends(get_get_user_by_email_use_case)
) -> User:
    try:
        user = await use_case.execute(email=email)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(
    login: str,
    email: str,
    password: str,
    first_name: str | None = None,
    second_name: str | None = None,
    use_case = Depends(get_create_user_use_case)
) -> User:
    try:
        user = await use_case.execute(
            login=login,
            email=email,
            password=password,
            first_name=first_name,
            second_name=second_name
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{user_id}/login", status_code=status.HTTP_200_OK, response_model=User)
async def update_user_login(
    user_id: int,
    new_login: str,
    use_case = Depends(get_update_user_login_use_case)
) -> User:
    try:
        user = await use_case.execute(
            user_id=user_id,
            new_login=new_login
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{user_id}/email", status_code=status.HTTP_200_OK, response_model=User)
async def update_user_email(
    user_id: int,
    new_email: str,
    use_case = Depends(get_update_user_email_use_case)
) -> User:
    try:
        user = await use_case.execute(
            user_id=user_id,
            new_email=new_email
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{user_id}/password", status_code=status.HTTP_200_OK, response_model=User)
async def update_user_password(
    user_id: int,
    new_password: str,
    use_case = Depends(get_update_user_password_use_case)
) -> User:
    try:
        user = await use_case.execute(
            user_id=user_id,
            new_password=new_password
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{user_id}/name", status_code=status.HTTP_200_OK, response_model=User)
async def update_user_name(
    user_id: int,
    first_name: str | None = None,
    second_name: str | None = None,
    use_case = Depends(get_update_user_name_use_case)
) -> User:
    try:
        user = await use_case.execute(
            user_id=user_id,
            first_name=first_name,
            second_name=second_name
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    use_case = Depends(get_delete_user_use_case)
):
    try:
        result = await use_case.execute(user_id=user_id)
        if result:
            return {"message": f"Пользователь с id {user_id} успешно удален"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
