from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import Field

from app.domain.place import Place

class MongoPlaceRepository:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.database = database
        self.collection = database["Places"]
    
    async def get_all(self) -> List[Place]:
        cursor = self.collection.find()

        places = []
        
        async for document in cursor:
            place = MongoPlace.model_validate(document)
            places.append(place)

        return places
    
    async def get_by_id(self, place_id: int) -> Optional[Place]:
        document = await self.collection.find_one({"_id": place_id})

        if document is None:
            return None
        
        place = MongoPlace.model_validate(document) 

        return place

    async def get_by_str_id(self, place_id: str) -> Optional[Place]:
        obj_id = ObjectId(place_id)

        document = await self.collection.find_one({"_id": obj_id})

        if document is None:
            return None

        place = MongoPlace.model_validate(document)

        return place
    
    async def save(self, place: Place):

        if not hasattr(place, 'version'):
            mongo_place = MongoPlace(**place.model_dump())
            await self.collection.insert_one(mongo_place.model_dump(by_alias=True))

            return
        
        place.version += 1

        await self.collection.replace_one(
                { "_id": place.place_id },
                place.model_dump())

    async def find_by_disability_types(self, disability_types: List[str]) -> List[Place]:
        query = {}
        if disability_types:

            disability_types_str = [disability_type.value for disability_type in disability_types]

            query = {
                "facilities": {
                    "$elemMatch": {
                        "disability_types": {"$all": disability_types_str}
                    }
                }
            }

        cursor = self.collection.find(query)
        results = []
        async for document in cursor:
            place = MongoPlace.model_validate(document)
            results.append(place)

        return results


class MongoPlace(Place):
    place_id: str = Field(alias="_id")
    version: int = 0

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True

