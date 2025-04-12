from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from typing import List, Optional

from app.di import get_place_repository
from app.domain.location import Location
from app.domain.place import Place
from app.domain.placeType import PlaceType
from app.infrastructure.mongoPlaceRepository import MongoPlaceRepository
from app.schemas.placeSchemas import CreatePlaceRequest, CreatePlaceResponse, GetPlacesResponse


router = APIRouter()

@router.get("/places", response_model=GetPlacesResponse)
async def get_places(place_repository: MongoPlaceRepository = Depends(get_place_repository)):

    places = await place_repository.get_all();

    return GetPlacesResponse(places=places)

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
