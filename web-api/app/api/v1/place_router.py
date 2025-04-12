from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.di import get_place_repository
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