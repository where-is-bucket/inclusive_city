from pydantic import BaseModel


class PlaceType(BaseModel):
    type_name: str