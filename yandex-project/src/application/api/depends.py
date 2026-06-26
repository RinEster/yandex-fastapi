from application.domain.auth.use_cases.authenticate_user import (
    AuthenticateUserUseCase,
)
from application.domain.auth.use_cases.create_access_token import (
    CreateAccessTokenUseCase,
)
from application.domain.category.use_cases.create_category import (
    CreateCategoryUseCase,
)
from application.domain.category.use_cases.delete_category import (
    DeleteCategoryUseCase,
)
from application.domain.category.use_cases.get_all_categories import (
    GetAllCategoriesUseCase,
)
from application.domain.category.use_cases.get_by_slug import (
    GetCategoryBySlugUseCase,
)
from application.domain.category.use_cases.get_category_by_id import (
    GetCategoryByIdUseCase,
)
from application.domain.category.use_cases.get_published import (
    GetPublishedCategoriesUseCase,
)
from application.domain.category.use_cases.update_category import (
    UpdateCategoryUseCase,
)
from application.domain.comment.use_cases.create_comment import (
    CreateCommentUseCase,
)
from application.domain.comment.use_cases.delete_comment import (
    DeleteCommentUseCase,
)
from application.domain.comment.use_cases.get_comment_by_id import (
    GetCommentByIdUseCase,
)
from application.domain.comment.use_cases.get_comment_by_post import (
    GetCommentsByPostUseCase,
)
from application.domain.comment.use_cases.update_comment import (
    UpdateCommentUseCase,
)
from application.domain.location.use_cases.create_location import (
    CreateLocationUseCase,
)
from application.domain.location.use_cases.delete_location import (
    DeleteLocationUseCase,
)
from application.domain.location.use_cases.get_all_locations import (
    GetAllLocationsUseCase,
)
from application.domain.location.use_cases.get_location_by_id import (
    GetLocationByIdUseCase,
)
from application.domain.location.use_cases.get_published import (
    GetPublishedLocationsUseCase,
)
from application.domain.location.use_cases.update_location import (
    UpdateLocationUseCase,
)
from application.domain.post.use_cases.create_post import (
    CreatePostUseCase,
)
from application.domain.post.use_cases.delete_post import (
    DeletePostUseCase,
)
from application.domain.post.use_cases.get_all_posts import (
    GetAllPostsUseCase,
)
from application.domain.post.use_cases.get_post_by_id import (
    GetPostByIdUseCase,
)
from application.domain.post.use_cases.get_published import (
    GetPublishedPostsUseCase,
)
from application.domain.post.use_cases.update_post import (
    UpdatePostUseCase,
)
from application.domain.user.use_cases.create_user import (
    CreateUserUseCase,
)
from application.domain.user.use_cases.delete_user import (
    DeleteUserUseCase,
)
from application.domain.user.use_cases.get_all_users import (
    GetAllUsersUseCase,
)
from application.domain.user.use_cases.get_user_by_email import (
    GetUserByEmailUseCase,
)
from application.domain.user.use_cases.get_user_by_id import (
    GetUserByIdUseCase,
)
from application.domain.user.use_cases.get_user_by_login import (
    GetUserByLoginUseCase,
)
from application.domain.user.use_cases.update_user import (
    UpdateUserUseCase,
)
from application.domain.post.use_cases.add_post_images import (
    AddPostImagesUseCase,
)
from application.domain.post.use_cases.get_post_images import (
    GetPostImagesUseCase,
)

from application.domain.post.use_cases.delete_single_image import (
    DeleteSingleImageUseCase,
)

from application.domain.post.use_cases.delete_all_images import (
    DeleteAllImagesUseCase,
)

from application.domain.comment.use_cases.add_comment_image import AddCommentImageUseCase
from application.domain.comment.use_cases.delete_single_image import DeleteSingleCommentImageUseCase
from application.domain.comment.use_cases.delete_all_image import DeleteAllCommentImagesUseCase
from application.domain.comment.use_cases.get_comment_image import GetCommentImagesUseCase


from application.domain.post.use_cases.get_by_category import   GetPostsByCategoryUseCase

def add_comment_image_use_case() -> AddCommentImageUseCase:
    return AddCommentImageUseCase()


def get_comment_images_use_case() -> GetCommentImagesUseCase:
    return GetCommentImagesUseCase()


def delete_all_comment_images_use_case() -> DeleteAllCommentImagesUseCase:
    return DeleteAllCommentImagesUseCase()


def delete_single_comment_image_use_case() -> DeleteSingleCommentImageUseCase:
    return DeleteSingleCommentImageUseCase()

def get_post_by_category_use_case() -> GetPostsByCategoryUseCase:
    return GetPostsByCategoryUseCase()

def add_post_images_use_case() -> AddPostImagesUseCase:
    return AddPostImagesUseCase()


def delete_single_image_use_case() -> DeleteSingleImageUseCase:
    return DeleteSingleImageUseCase()


def delete_all_images_use_case() -> DeleteAllImagesUseCase:
    return DeleteAllImagesUseCase()
def get_post_images_use_case() -> GetPostImagesUseCase:
    return GetPostImagesUseCase()
def authenticate_user_use_case() -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase()


def create_access_token_use_case() -> CreateAccessTokenUseCase:
    return CreateAccessTokenUseCase()


def get_all_posts_use_case() -> GetAllPostsUseCase:
    return GetAllPostsUseCase()


def get_post_by_id_use_case() -> GetPostByIdUseCase:
    return GetPostByIdUseCase()


def create_post_use_case() -> CreatePostUseCase:
    return CreatePostUseCase()


def update_post_use_case() -> UpdatePostUseCase:
    return UpdatePostUseCase()


def delete_post_use_case() -> DeletePostUseCase:
    return DeletePostUseCase()


def get_published_post_use_case() -> GetPublishedPostsUseCase:
    return GetPublishedPostsUseCase()


def create_category_use_case() -> CreateCategoryUseCase:
    return CreateCategoryUseCase()


def get_category_by_slug_use_case() -> GetCategoryBySlugUseCase:
    return GetCategoryBySlugUseCase()


def get_all_categories_use_case() -> GetAllCategoriesUseCase:
    return GetAllCategoriesUseCase()


def get_category_by_id_use_case() -> GetCategoryByIdUseCase:
    return GetCategoryByIdUseCase()


def get_published_categories_use_case() -> (
    GetPublishedCategoriesUseCase
):
    return GetPublishedCategoriesUseCase()


def update_category_use_case() -> UpdateCategoryUseCase:
    return UpdateCategoryUseCase()


def delete_category_use_case() -> DeleteCategoryUseCase:
    return DeleteCategoryUseCase()


def create_comment_use_case() -> CreateCommentUseCase:
    return CreateCommentUseCase()


def get_comment_by_id_use_case() -> GetCommentByIdUseCase:
    return GetCommentByIdUseCase()


def get_comments_by_post_use_case() -> GetCommentsByPostUseCase:
    return GetCommentsByPostUseCase()


def update_comment_use_case() -> UpdateCommentUseCase:
    return UpdateCommentUseCase()


def delete_comment_use_case() -> DeleteCommentUseCase:
    return DeleteCommentUseCase()


def create_location_use_case() -> CreateLocationUseCase:
    return CreateLocationUseCase()


def get_all_locations_use_case() -> GetAllLocationsUseCase:
    return GetAllLocationsUseCase()


def get_location_by_id_use_case() -> GetLocationByIdUseCase:
    return GetLocationByIdUseCase()


def get_published_locations_use_case() -> (
    GetPublishedLocationsUseCase
):
    return GetPublishedLocationsUseCase()


def update_location_use_case() -> UpdateLocationUseCase:
    return UpdateLocationUseCase()


def delete_location_use_case() -> DeleteLocationUseCase:
    return DeleteLocationUseCase()


def create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase()


def get_user_by_id_use_case() -> GetUserByIdUseCase:
    return GetUserByIdUseCase()


def get_user_by_login_use_case() -> GetUserByLoginUseCase:
    return GetUserByLoginUseCase()


def get_user_by_email_use_case() -> GetUserByEmailUseCase:
    return GetUserByEmailUseCase()


def get_all_users_use_case() -> GetAllUsersUseCase:
    return GetAllUsersUseCase()


def update_user_use_case() -> UpdateUserUseCase:
    return UpdateUserUseCase()


def delete_user_use_case() -> DeleteUserUseCase:
    return DeleteUserUseCase()
