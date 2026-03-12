from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from datetime import datetime
from schemas.categories import Category

categories_router = APIRouter()

from api.depends import (
    get_create_category_use_case,
    get_get_all_categories_use_case,
    get_get_category_by_id_use_case,
    get_get_published_categories_use_case,
    get_update_category_use_case,
    get_delete_category_use_case
)


# получение всех существующих категорий
@categories_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Category])
async def get_categories(
    use_case = Depends(get_get_all_categories_use_case)
) -> List[Category]:
    categories = await use_case.execute()
    return categories

@categories_router.get("/published", status_code=status.HTTP_200_OK, response_model=List[Category])
async def get_published_categories(
    use_case = Depends(get_get_published_categories_use_case)
) -> List[Category]:
    categories = await use_case.execute()
    return categories

# получение категории по конкретному id
@categories_router.get("/{category_id}", status_code=status.HTTP_200_OK, response_model=Category)
async def get_category(
    category_id: int,
    use_case = Depends(get_get_category_by_id_use_case)
) -> Category:
    try:
        category = await use_case.execute(category_id=category_id)
        return category
    except ValueError as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_404_NOT_FOUND
        )


# добавление категории
@categories_router.post("/add", status_code=status.HTTP_201_CREATED, response_model=Category)
async def create_category(
    title: str,
    description: str,
    slug: str,
    is_published: bool,
    use_case = Depends(get_create_category_use_case)
) -> Category:
    try:
        category = await use_case.execute(
            title=title,
            description=description,
            slug=slug,
            is_published=is_published
        )
        return category
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# удаление категории
@categories_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    use_case = Depends(get_delete_category_use_case)
):
    try:
        await use_case.execute(category_id=category_id)
        return
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# обновление категории
@categories_router.put("/update/{category_id}", status_code=status.HTTP_200_OK, response_model=Category)
async def update_category(
    category_id: int,
    new_title: str,
    new_description: str,
    new_slug: str,
    new_is_published: bool,
    use_case = Depends(get_update_category_use_case)
) -> Category:
    try:
        category = await use_case.execute(
            category_id=category_id,
            title=new_title,
            description=new_description,
            slug=new_slug,
            is_published=new_is_published
        )
        return category
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
