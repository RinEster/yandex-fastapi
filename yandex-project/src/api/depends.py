from domain.user.use_cases.create_user import CreateUserUseCase
from domain.user.use_cases.get_user_by_id import GetUserByIdUseCase
from domain.user.use_cases.get_user_by_login import GetUserByLoginUseCase
from domain.user.use_cases.get_user_by_email import GetUserByEmailUseCase
from domain.user.use_cases.get_all_users import GetAllUsersUseCase
from domain.user.use_cases.update_user_login import UpdateUserLoginUseCase
from domain.user.use_cases.update_user_email import UpdateUserEmailUseCase
from domain.user.use_cases.update_user_password import UpdateUserPasswordUseCase
from domain.user.use_cases.update_user_name import UpdateUserNameUseCase
from domain.user.use_cases.delete_user import DeleteUserUseCase

def get_create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase()

def get_get_user_by_id_use_case() -> GetUserByIdUseCase:
    return GetUserByIdUseCase()

def get_get_user_by_login_use_case() -> GetUserByLoginUseCase:
    return GetUserByLoginUseCase()

def get_get_user_by_email_use_case() -> GetUserByEmailUseCase:
    return GetUserByEmailUseCase()

def get_get_all_users_use_case() -> GetAllUsersUseCase:
    return GetAllUsersUseCase()

def get_update_user_login_use_case() -> UpdateUserLoginUseCase:
    return UpdateUserLoginUseCase()

def get_update_user_email_use_case() -> UpdateUserEmailUseCase:
    return UpdateUserEmailUseCase()

def get_update_user_password_use_case() -> UpdateUserPasswordUseCase:
    return UpdateUserPasswordUseCase()

def get_update_user_name_use_case() -> UpdateUserNameUseCase:
    return UpdateUserNameUseCase()

def get_delete_user_use_case() -> DeleteUserUseCase:
    return DeleteUserUseCase()
