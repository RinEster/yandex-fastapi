from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from schemas.locations import LocationResponce, LocationCreate, LocationUpdate
locations_router = APIRouter()

from api.depends import (
    create_location_use_case,
    get_all_locations_use_case,
    get_location_by_id_use_case,
    get_published_locations_use_case,
    update_location_use_case,
    delete_location_use_case
)

from core.exceptions.domain_exception import(
    LocationNotFoundByIdException,
    LocationTitleIsNotUniqueException
)


@locations_router.get("/",
                      status_code=status.HTTP_200_OK,
                      response_model=List[LocationResponce]
                      )
async def get_all_locations(
    use_case = Depends(get_all_locations_use_case)
) -> List[LocationResponce]:
    locations = await use_case.execute()
    return locations


@locations_router.get("/published",
                      status_code=status.HTTP_200_OK,
                      response_model=List[LocationResponce]
                      )
async def get_published_locations(
    use_case = Depends(get_published_locations_use_case)
) -> List[LocationResponce]:
    locations = await use_case.execute()
    return locations


@locations_router.get("/{location_id}",
                      status_code=status.HTTP_200_OK,
                      response_model=LocationResponce)
async def get_location_by_id(
    location_id: int,
    use_case = Depends(get_location_by_id_use_case)
) -> LocationResponce:
    try:
        location = await use_case.execute(location_id=location_id)
        return location
    except LocationNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@locations_router.post("/add",
                       status_code=status.HTTP_201_CREATED,
                       response_model=LocationResponce)
async def create_location(
    data: LocationCreate,
    use_case = Depends(create_location_use_case)
) -> LocationResponce:
    try:
        location = await use_case.execute(data=data)
        return location
    except LocationTitleIsNotUniqueException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"Ошибка при создании локации: {str(e)}"
        )


@locations_router.put("/{location_id}",
                      status_code=status.HTTP_200_OK,
                      response_model=LocationResponce)
async def update_location(
    location_id: int,
    data: LocationUpdate,
    use_case = Depends(update_location_use_case)
) -> LocationResponce:
    try:
        location = await use_case.execute(
            location_id=location_id,
            data=data
        )
        return location
    except LocationNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except LocationTitleIsNotUniqueException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
        

@locations_router.delete("/{location_id}",
                         status_code=status.HTTP_200_OK)
async def delete_location(
    location_id: int,
    use_case = Depends(delete_location_use_case)
):
    try:
        result = await use_case.execute(location_id=location_id)
        if result:
            return 
    except LocationNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
