from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from datetime import datetime
from schemas.categories import CategoryResponse, CategoryCreate, CategoryUpdate

categories_router = APIRouter()

from api.depends import (
    create_category_use_case,
    get_all_categories_use_case,
    get_category_by_id_use_case,
    get_category_by_slug_use_case,
    get_published_categories_use_case,
    update_category_use_case,
    delete_category_use_case
)

from core.exceptions.domain_exception import (
    CategoryNotFoundByIdException,
    CategoryNotFoundBySlugException,
    CategoryTitleIsNotUniqueException,
    CategorySlugIsNotUniqueException
)


# получение всех существующих категорий
@categories_router.get("/", status_code=status.HTTP_200_OK, response_model=List[CategoryResponse])
async def get_categories(
    use_case = Depends(get_all_categories_use_case)
) -> List[CategoryResponse]:
    categories = await use_case.execute()
    return categories


# получение опубликованных категорий
@categories_router.get("/published", status_code=status.HTTP_200_OK, response_model=List[CategoryResponse])
async def get_published_categories(
    use_case = Depends(get_published_categories_use_case)
) -> List[CategoryResponse]:
    categories = await use_case.execute()
    return categories


# получение категории по id
@categories_router.get("/by-id/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryResponse)
async def get_category_by_id(
    category_id: int,
    use_case = Depends(get_category_by_id_use_case)
) -> CategoryResponse:
    try:
        category = await use_case.execute(category_id=category_id)
        return category
    except CategoryNotFoundByIdException as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_404_NOT_FOUND
        )


# получение категории по slug
@categories_router.get("/by-slug/{slug}", status_code=status.HTTP_200_OK, response_model=CategoryResponse)
async def get_category_by_slug(
    slug: str,
    use_case = Depends(get_category_by_slug_use_case)
) -> CategoryResponse:
    try:
        category = await use_case.execute(slug=slug)
        return category
    except CategoryNotFoundBySlugException as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_404_NOT_FOUND
        )


# добавление категории
@categories_router.post("/add", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
async def create_category(
    data: CategoryCreate,
    use_case = Depends(create_category_use_case)
) -> CategoryResponse:
    try:
        category = await use_case.execute(data=data)
        return category
    except (CategoryTitleIsNotUniqueException, CategorySlugIsNotUniqueException) as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка при создании категории: {str(e)}"
        )


# удаление категории
@categories_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    use_case = Depends(delete_category_use_case)
):
    try:
        await use_case.execute(category_id=category_id)
        return
    except CategoryNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# обновление категории
@categories_router.put("/update/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryResponse)
async def update_category(
    category_id: int,
    data: CategoryUpdate,
    use_case = Depends(update_category_use_case)
) -> CategoryResponse:
    try:
        category = await use_case.execute(
            category_id=category_id,
            data=data
        )
        return category
    except CategoryNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except (CategoryTitleIsNotUniqueException, CategorySlugIsNotUniqueException) as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
