
from typing import List
from fastapi import APIRouter, Depends

from app.di import get_facility_repository
from app.domain.facility import Facility
from app.infrastructure.mongoPlaceRepository import MongoPlaceRepository


router = APIRouter()

@router.get("/facilities", response_model=List[Facility])
async def get_facilities(repository: MongoPlaceRepository = Depends(get_facility_repository)):
    return await repository.get_all();