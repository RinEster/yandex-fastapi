from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from schemas.locations import Location
locations_router = APIRouter()

from api.depends import (
    get_create_location_use_case,
    get_get_all_locations_use_case,
    get_get_location_by_id_use_case,
    get_get_published_locations_use_case,
    get_update_location_name_use_case,
    get_delete_location_use_case
)


@locations_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Location])
async def get_all_locations(
    use_case = Depends(get_get_all_locations_use_case)
) -> List[Location]:
    locations = await use_case.execute()
    return locations


@locations_router.get("/published", status_code=status.HTTP_200_OK, response_model=List[Location])
async def get_published_locations(
    use_case = Depends(get_get_published_locations_use_case)
) -> List[Location]:
    locations = await use_case.execute()
    return locations


@locations_router.get("/{location_id}", status_code=status.HTTP_200_OK, response_model=Location)
async def get_location_by_id(
    location_id: int,
    use_case = Depends(get_get_location_by_id_use_case)
) -> Location:
    try:
        location = await use_case.execute(location_id=location_id)
        return location
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@locations_router.post("/add", status_code=status.HTTP_201_CREATED, response_model=Location)
async def create_location(
    name: str,
    is_published: bool = True,
    use_case = Depends(get_create_location_use_case)
) -> Location:
    try:
        location = await use_case.execute(
            name=name,
            is_published=is_published
        )
        return location
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@locations_router.put("/{location_id}/name", status_code=status.HTTP_200_OK, response_model=Location)
async def update_location_name(
    location_id: int,
    new_name: str,
    use_case = Depends(get_update_location_name_use_case)
) -> Location:
    try:
        location = await use_case.execute(
            location_id=location_id,
            new_name=new_name
        )
        return location
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

        

@locations_router.delete("/{location_id}", status_code=status.HTTP_200_OK)
async def delete_location(
    location_id: int,
    use_case = Depends(get_delete_location_use_case)
):
    try:
        result = await use_case.execute(location_id=location_id)
        if result:
            return {
                "message": "Локация удалена",
                "success": True
            }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
