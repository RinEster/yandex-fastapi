from fastapi import APIRouter, status, HTTPException
from datetime import datetime
from schemas.users import User
from pydantic import SecretStr, EmailStr

users_router = APIRouter()

users = []
next_id = 1


#получение всех существующих пользователей
@users_router.get("/", status_code=status.HTTP_200_OK, response_model=list[User])
async def get_users() -> list:
    return users

#получение пользователя по конкретному id
@users_router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=User)
async def get_user(user_id: int) -> User:   
    for user in users:
        if user.id == user_id:
            return user
    
    raise HTTPException(
        detail="Пользователь не найден",
        status_code=status.HTTP_404_NOT_FOUND
    )

#добавление категории
@users_router.post("/add", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(login: str, email: str, password: str, first_name: str = None, second_name: str = None) -> User:
    global next_id
    new_user = User(
        id=next_id,
        login=login,
        email=email,
        password=password,
        first_name=first_name,
        second_name=second_name
    )

    users.append(new_user)
    next_id += 1

    return new_user