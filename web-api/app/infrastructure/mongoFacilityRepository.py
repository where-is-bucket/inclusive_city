from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import field_serializer, root_validator

from app.domain.disabilityTypes import DisabilityType
from app.domain.facility import Facility


class MongoFacilityRepository:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.database = database
        self.collection = database["Facilities"]
    
    async def get_all(self) -> List[Facility]:
        cursor = self.collection.find()

        facilities = []
        
        async for document in cursor:
            place = Facility.model_validate(document)
            facilities.append(place)

        return facilities
    
    async def save(self, facility: Facility):

        mongoFacility = MongoFacility(**facility.model_dump())

        await self.collection.insert_one(mongoFacility.model_dump())
        
        

class MongoFacility(Facility):

    @field_serializer("facility_id", when_used="json")
    def serialize_id(self, facility_id: Optional[str], _info):
        return ObjectId(facility_id) if facility_id else None

    @root_validator(pre=True)
    def map_mongo_id_to_place_id(cls, values):
        if "_id" in values:

            # MongoDB returns `_id`, but we map it to `place_id`
            values["facility_id"] = str(values["_id"])  # ObjectId to str
            del values["_id"]
        return values

    class Config:
        populate_by_name = True
        

