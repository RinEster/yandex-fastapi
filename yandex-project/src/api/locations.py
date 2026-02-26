from fastapi import APIRouter, status, HTTPException
from datetime import datetime
from schemas.locations import Location
locations_router = APIRouter()

locations = []
next_id = 1

@locations_router.get("/", status_code=status.HTTP_200_OK,response_model=list[Location])
async def get_locations()-> list:
    return locations

@locations_router.get("/{location_id}",status_code=status.HTTP_200_OK, response_model=Location)
async def get_location(location_id : int)->Location:
    for location in locations:
        if location.id == location_id:
            return location
    
    raise HTTPException(
        detail="Локация не найдена",
        status_code=status.HTTP_404_NOT_FOUND
    )

@locations_router.post("/add", status_code=status.HTTP_201_CREATED, response_model=Location)
async def create_location(name:str, is_published:bool)->Location:
    global next_id
    new_location = Location(
        id=next_id,
        name=name,
        is_published=is_published,
        created_at=datetime.now()
    )

    locations.append(new_location)
    next_id += 1

    return new_location
    
    
