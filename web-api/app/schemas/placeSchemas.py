from typing import List, Optional
from pydantic import BaseModel

from app.domain.place import Place

class CreatePlaceRequest(BaseModel):
    place_name: str
    place_types: List[str] = []
    google_photo_url: str
    google_id: str
    description: str
    address: str
    latitude: int
    longitude: int

class CreatePlaceResponse(BaseModel):
    place_id: str

class GetPlacesResponse(BaseModel):
    places: List[Place] = []