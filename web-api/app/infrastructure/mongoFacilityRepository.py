from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import Field

from app.domain.facility import Facility


class MongoFacilityRepository:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.database = database
        self.collection = database["Facilities"]
    
    async def get_by_id(self, facility_id: int) -> Optional[Facility]:
        document = await self.collection.find_one({"_id": facility_id})

        if document is None:
            return None
        
        place = MongoFacility.model_validate(document) 

        return place
    
    async def get_all(self) -> List[Facility]:
        cursor = self.collection.find()

        facilities = []
        
        async for document in cursor:
            place = MongoFacility.model_validate(document)
            facilities.append(place)

        return facilities
    
    async def save(self, facility: Facility):

        if not hasattr(facility, 'version'):
            mongo_facility = MongoFacility(**facility.model_dump())
            await self.collection.insert_one(mongo_facility.model_dump(by_alias=True))

            return
        
        facility.version += 1

        await self.collection.replace_one(
            { "_id": facility.facility_id },
            facility.model_dump())
        
        

class MongoFacility(Facility):
    facility_id: str = Field(alias="_id")
    version: int = 0

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
        

