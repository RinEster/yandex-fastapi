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

from domain.location.use_cases.create_location import CreateLocationUseCase
from domain.location.use_cases.get_all_locations import GetAllLocationsUseCase
from domain.location.use_cases.get_location_by_id import GetLocationByIdUseCase
from domain.location.use_cases.get_published import GetPublishedLocationsUseCase
from domain.location.use_cases.update_name_location import UpdateLocationNameUseCase
from domain.location.use_cases.delete_location import DeleteLocationUseCase


from domain.category.use_cases.create_category import CreateCategoryUseCase
from domain.category.use_cases.get_all_categories import GetAllCategoriesUseCase
from domain.category.use_cases.get_category_by_id import GetCategoryByIdUseCase
from domain.category.use_cases.get_published import GetPublishedCategoriesUseCase
from domain.category.use_cases.update_category import UpdateCategoryUseCase
from domain.category.use_cases.delete_category import DeleteCategoryUseCase

from domain.posts.use_cases.get_all_posts import GetAllPostsUseCase
from domain.posts.use_cases.get_post_by_id import GetPostByIdUseCase
from domain.posts.use_cases.create_post import CreatePostUseCase
from domain.posts.use_cases.update_post import UpdatePostUseCase
from domain.posts.use_cases.delete_post import DeletePostUseCase


def get_get_all_posts_use_case() -> GetAllPostsUseCase:
    return GetAllPostsUseCase()


def get_get_post_by_id_use_case() -> GetPostByIdUseCase:
    return GetPostByIdUseCase()


def get_create_post_use_case() -> CreatePostUseCase:
    return CreatePostUseCase()


def get_update_post_use_case() -> UpdatePostUseCase:
    return UpdatePostUseCase()


def get_delete_post_use_case() -> DeletePostUseCase:
    return DeletePostUseCase()


def get_create_category_use_case() -> CreateCategoryUseCase:
    return CreateCategoryUseCase()


def get_get_all_categories_use_case() -> GetAllCategoriesUseCase:
    return GetAllCategoriesUseCase()


def get_get_category_by_id_use_case() -> GetCategoryByIdUseCase:
    return GetCategoryByIdUseCase()


def get_get_published_categories_use_case() -> GetPublishedCategoriesUseCase:
    return GetPublishedCategoriesUseCase()


def get_update_category_use_case() -> UpdateCategoryUseCase:
    return UpdateCategoryUseCase()


def get_delete_category_use_case() -> DeleteCategoryUseCase:
    return DeleteCategoryUseCase()


def get_create_location_use_case() -> CreateLocationUseCase:
    return CreateLocationUseCase()


def get_get_all_locations_use_case() -> GetAllLocationsUseCase:
    return GetAllLocationsUseCase()


def get_get_location_by_id_use_case() -> GetLocationByIdUseCase:
    return GetLocationByIdUseCase()


def get_get_published_locations_use_case() -> GetPublishedLocationsUseCase:
    return GetPublishedLocationsUseCase()


def get_update_location_name_use_case() -> UpdateLocationNameUseCase:
    return UpdateLocationNameUseCase()


def get_delete_location_use_case() -> DeleteLocationUseCase:
    return DeleteLocationUseCase()


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
