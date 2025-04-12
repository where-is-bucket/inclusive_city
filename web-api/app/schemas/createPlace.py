from pydantic import BaseModel


class CreatePlaceRequest(BaseModel):
    place_name: str
    place_type: str
    description: str
    address: str
    latitude: int
    longitude: int

class CreatePlaceResponse(BaseModel):
    place_id: str