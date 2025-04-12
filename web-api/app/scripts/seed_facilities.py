import json

from app.domain.disabilityTypes import DisabilityType
from app.domain.facility import Facility

from motor.motor_asyncio import AsyncIOMotorClient

from app.infrastructure.mongoFacilityRepository import MongoFacilityRepository

data = []

MONGO_URI = "mongodb://localhost:27017?directConnection=true"

client = AsyncIOMotorClient(MONGO_URI)
database = client["MyDb"]
repository = MongoFacilityRepository(database)

import asyncio

async def main():
    with open('./app/scripts/sample_facilities.json', 'r', encoding='utf-8') as f:
     data = json.load(f)

    for item in data:
     text = text=item.get('text')
     disability_types = [DisabilityType[d] for d in item["disability_types"]]
     
     facility = Facility.create(
          text=text,
          disability_types=disability_types)
     
     await repository.save(facility)    

asyncio.run(main())
