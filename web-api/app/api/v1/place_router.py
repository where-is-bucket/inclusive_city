from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List, Optional, Union

from app.di import get_facility_repository, get_place_repository
from app.domain.disabilityTypes import DisabilityType
from app.domain.location import Location
from app.domain.place import Place
from app.domain.placeType import PlaceType
from app.infrastructure.mongoFacilityRepository import MongoFacilityRepository
from app.infrastructure.mongoPlaceRepository import MongoPlaceRepository
from app.schemas.placeSchemas import CreatePlaceRequest, CreatePlaceResponse


router = APIRouter()

@router.get("/places", response_model=List[Place])
async def get_places(place_repository: MongoPlaceRepository = Depends(get_place_repository)):

    return await place_repository.get_all()

@router.get("/places/{place_id}", response_model=Place)
async def get_by_id(
    place_id: str,
    place_repository: MongoPlaceRepository = Depends(get_place_repository)):

    return await place_repository.get_by_id(place_id=place_id);

@router.post("/places", response_model=CreatePlaceResponse)
async def create_place(
    request: CreatePlaceRequest,
    place_repository: MongoPlaceRepository = Depends(get_place_repository)):

    location = Location(request.latitude, request.longitude)

    place = Place(
        place_id=request.google_id,
        place_name=request.place_name,
        place_types=request.place_types,
        address=request.address,
        description=request.description,
        google_photo_url=request.google_photo_url or "",
        location=location)
    
    await place_repository.save(place)

    response = CreatePlaceResponse(place_id = place.place_id)

    return response


@router.get("/place", response_model=List[Place])
async def get_places_by_disability_types(
        disability_types: List[DisabilityType] = Query(default=[]),
        place_repository: MongoPlaceRepository = Depends(get_place_repository)):

    places = await place_repository.find_by_disability_types(disability_types)

    return places


@router.put("/place/{place_id}/facilities/{facility_id}", response_model=None)
async def update_place_facilities(
    place_id: str,
    facility_id: str,
    facility_repository: MongoFacilityRepository = Depends(get_facility_repository),
    place_repository: MongoPlaceRepository = Depends(get_place_repository)):

    facility = await facility_repository.get_by_id(facility_id=facility_id)
    place = await place_repository.get_by_id(place_id=place_id)

    if facility is None:
        HTTPException(status_code=404, detail="Facility not found")

    if place is None:
        HTTPException(status_code=404, detail="Place not found")
    
    place.add_facility(addedFacility=facility)

    await place_repository.save(place)

@router.delete("/place/{place_id}/facilities/{facility_id}", response_model=None)
async def delete_place_facilities(
    place_id: str,
    facility_id: str,
    facility_repository: MongoFacilityRepository = Depends(get_facility_repository),
    place_repository: MongoPlaceRepository = Depends(get_place_repository)):

    facility = await facility_repository.get_by_id(facility_id=facility_id)
    place = await place_repository.get_by_id(place_id=place_id)

    if facility is None:
        HTTPException(status_code=404, detail="Facility not found")

    if place is None:
        HTTPException(status_code=404, detail="Place not found")
    
    place.remove_facility(removedFacility=facility)

    await place_repository.save(place)