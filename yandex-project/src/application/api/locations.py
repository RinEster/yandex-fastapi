from typing import List

from application.core.exceptions.domain_exception import (
    LocationNotFoundByIdException,
    LocationTitleIsNotUniqueException,
)
from fastapi import APIRouter, Depends, HTTPException, status
from application.schemas.locations import (
    LocationCreate,
    LocationResponse,
    LocationUpdate,
)

from application.api.depends import (
    create_location_use_case,
    delete_location_use_case,
    get_all_locations_use_case,
    get_location_by_id_use_case,
    get_published_locations_use_case,
    update_location_use_case,
)

locations_router = APIRouter()


@locations_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[LocationResponse],
)
async def get_all_locations(
    use_case=Depends(get_all_locations_use_case),
) -> List[LocationResponse]:
    locations = await use_case.execute()
    return locations


@locations_router.get(
    "/published",
    status_code=status.HTTP_200_OK,
    response_model=List[LocationResponse],
)
async def get_published_locations(
    use_case=Depends(get_published_locations_use_case),
) -> List[LocationResponse]:
    locations = await use_case.execute()
    return locations


@locations_router.get(
    "/id/{location_id}",
    status_code=status.HTTP_200_OK,
    response_model=LocationResponse,
)
async def get_location_by_id(
    location_id: int, use_case=Depends(get_location_by_id_use_case)
) -> LocationResponse:
    try:
        location = await use_case.execute(location_id=location_id)
        return location
    except LocationNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@locations_router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    response_model=LocationResponse,
)
async def create_location(
    data: LocationCreate, use_case=Depends(create_location_use_case)
) -> LocationResponse:
    try:
        location = await use_case.execute(data=data)
        return location
    except LocationTitleIsNotUniqueException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ошибка при создании локации: {str(e)}",
        )


@locations_router.put(
    "/id/{location_id}",
    status_code=status.HTTP_200_OK,
    response_model=LocationResponse,
)
async def update_location(
    location_id: int,
    data: LocationUpdate,
    use_case=Depends(update_location_use_case),
) -> LocationResponse:
    try:
        location = await use_case.execute(
            location_id=location_id, data=data
        )
        return location
    except LocationNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except LocationTitleIsNotUniqueException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        )


@locations_router.delete(
    "/id/{location_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_location(
    location_id: int, use_case=Depends(delete_location_use_case)
):
    try:
        await use_case.execute(location_id=location_id)
    except LocationNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
