from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import field_serializer, root_validator

from app.domain.place import Place

class MongoPlaceRepository:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.database = database
        self.collection = database["Places"]
    
    async def get_all(self) -> List[Place]:
        cursor = self.collection.find()

        places = []
        
        async for document in cursor:
            place = Place.model_validate(document)
            places.append(place)

        return places
    
    async def get_by_id(self, place_id: int) -> Optional[Place]:
        obj_id = ObjectId(place_id)

        document = await self.collection.find_one({"_id": obj_id})

        if document is None:
            return None
        
        place = MongoPlace.model_validate(document) 

        return place
    
    async def save(self, place: Place):

        if place.place_id:
            place.version += 1

            await self.collection.replace_one(
                { "_id": ObjectId(place.place_id) },
                place.model_dump())
            
        else:
            mongoPlace = MongoPlace(**place.model_dump(), version=1)

            result = await self.collection.insert_one(mongoPlace.model_dump())

            place.place_id = str(result.inserted_id)
        
        

class MongoPlace(Place):
    version: int = 0

    @field_serializer("place_id", when_used="json")
    def serialize_id(self, place_id: Optional[str], _info):
        return ObjectId(place_id) if place_id else None

    @root_validator(pre=True)
    def map_mongo_id_to_place_id(cls, values):
        if "_id" in values:

            # MongoDB returns `_id`, but we map it to `place_id`
            values["place_id"] = str(values["_id"])  # ObjectId to str
            del values["_id"]
        return values

    class Config:
        populate_by_name = True
        

