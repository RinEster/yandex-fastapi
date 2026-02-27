from fastapi import APIRouter, status, HTTPException
from datetime import datetime
from schemas.categories import Category

categories_router = APIRouter()

categories = []
next_id = 1

#получение всех существующих категорий
@categories_router.get("/", status_code=status.HTTP_200_OK, response_model=list[Category])
async def get_categories() -> list:
    return categories

#получение категории по конкретному id
@categories_router.get("/{category_id}", status_code=status.HTTP_200_OK, response_model=Category)
async def get_category(category_id: int) -> Category:   
    for category in categories:
        if category.id == category_id:
            return category
    
    raise HTTPException(
        detail="Категория не найдена",
        status_code=status.HTTP_404_NOT_FOUND
    )

#добавление категории
@categories_router.post("/add", status_code=status.HTTP_201_CREATED, response_model=Category)
async def create_category(title: str, description : str, slug : str, is_published : bool) -> Category:
    global next_id
    new_category = Category(
        id=next_id,
        title=title,
        description=description,
        slug=slug,
        is_published=is_published,
        created_at=datetime.now()
    )

    categories.append(new_category)
    next_id += 1

    return new_category

#удаление категории
@categories_router.delete("/{category_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id:int):
    global categories
    
    for category in categories:
        if category.id == category_id:
            deleted = categories.remove(category)
            return
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Категория не найдена"
    )

@categories_router.put("/update/{category_id}", status_code=status.HTTP_200_OK, response_model=Category)    
async def update_category(category_id : int, new_title: str, new_description : str, new_slug : str, new_is_published : bool):
    for category in categories:
        if category.id == category_id:
            category.title = new_title
            category.description = new_description
            category.slug = new_slug
            category.is_published = new_is_published
            return category
    

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Категория не найдена"
    )

    
    
    
    
    
