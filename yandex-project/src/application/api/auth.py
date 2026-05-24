from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from pydantic import EmailStr, SecretStr

users_router = APIRouter()

from typing import Annotated

from application.core.exceptions.domain_exception import (
    UserNotFoundByLoginException,
    WrongPasswordException,
)
from application.domain.auth.use_cases.authenticate_user import (
    AuthenticateUserUseCase,
)
from application.domain.auth.use_cases.create_access_token import (
    CreateAccessTokenUseCase,
)
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from application.schemas.auth import Token

from application.api.depends import (
    authenticate_user_use_case,
    create_access_token_use_case,
)

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_use_case: Annotated[
        AuthenticateUserUseCase, Depends(authenticate_user_use_case)
    ],
    create_token_use_case: CreateAccessTokenUseCase = Depends(
        create_access_token_use_case
    ),
) -> Token:
    try:
        user = await auth_use_case.execute(
            login=form_data.username, password=form_data.password
        )
    except WrongPasswordException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.get_detail(),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except UserNotFoundByLoginException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )

    access_token = await create_token_use_case.execute(
        login=user.login
    )

    return Token(access_token=access_token, token_type="bearer")
