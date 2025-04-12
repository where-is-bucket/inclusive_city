from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional

from pydantic import BaseModel

from app.di import get_place_repository
from app.domain.facility import Facility
from app.domain.location import Location
from app.domain.place import Place
from app.domain.placeType import PlaceType
from app.infrastructure.mongoPlaceRepository import MongoPlaceRepository
from app.schemas.createPlace import CreatePlaceRequest, CreatePlaceResponse

router = APIRouter()

@router.post("/place", response_model=CreatePlaceResponse)
async def create_place(
    request: CreatePlaceRequest,
    place_repository: MongoPlaceRepository = Depends(get_place_repository)):

    location = Location(request.latitude, request.longitude)

    place_type = PlaceType(type_name=request.place_type)

    place = Place(
        place_name=request.place_name,
        place_type=place_type,
        address=request.address,
        description=request.description,
        location=location)
    
    await place_repository.save(place)

    response = CreatePlaceResponse(place_id = place.place_id)

    return response


@router.get("/place", response_model=List[Place])
async def get_places_by_disability_types(
        disability_types: List[str] = Query(default=[]),
        place_repository: MongoPlaceRepository = Depends(get_place_repository)):

    places = await place_repository.find_by_disability_types(disability_types)

    return places


class UpdateFacilitiesRequest(BaseModel):
    facilities: List[Facility]


@router.put("/place/{place_id}/facilities", response_model=CreatePlaceResponse)
async def update_place_facilities(
        place_id: str,
        request: UpdateFacilitiesRequest,
        place_repository: MongoPlaceRepository = Depends(get_place_repository)):
    try:
        await place_repository.update_facilities(place_id, request.facilities)
        return CreatePlaceResponse(place_id=place_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Place not found")
