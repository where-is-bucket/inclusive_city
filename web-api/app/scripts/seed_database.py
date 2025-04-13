import asyncio
import json
import sys

from motor.motor_asyncio import AsyncIOMotorClient

from pymongo.errors import DuplicateKeyError

from app.domain.disabilityTypes import DisabilityType
from app.domain.facility import Facility
from app.domain.location import Location
from app.domain.place import Place
from app.domain.placeType import PlaceType
from app.infrastructure.mongoFacilityRepository import MongoFacilityRepository
from app.infrastructure.mongoPlaceRepository import MongoPlaceRepository

MONGO_URI = "mongodb://localhost:27017?directConnection=true"

client = AsyncIOMotorClient(MONGO_URI)
database = client["MyDb"]
facilityRepository = MongoFacilityRepository(database)
placeRepository = MongoPlaceRepository(database)

async def seed_facilities(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

        for item in data:
            text = text=item.get('text')
            disability_types = [DisabilityType[d] for d in item["disability_types"]]
     
            facility = Facility.create(descriptive_name=text, disability_types=disability_types)
     
            await facilityRepository.save(facility)    

async def seed_places(path):
    facilities = await facilityRepository.get_all()

    facility_map = {facility.descriptive_name: facility for facility in facilities}

    data = []

    with open(path, 'r', encoding='utf-8') as f:
      data = json.load(f)

      for item in data:
        name = item.get('lun_name') or item.get('google_name')
        address  = item.get('lun_address') or item.get('google_address')
        google_id = item.get('google_place_id')

        if  name is None or address is None or google_id is None:
           continue

        coordinates = item.get('google_coordinates')
        latitude = coordinates.get('latitude')
        longitude = coordinates.get('longitude')
        
        inner_descriptions = item.get('lun_description', [])
        facility_name_list = [description.get('values') for description in inner_descriptions if description.get('values')]
        flat_names_list = [item for sublist in facility_name_list for item in sublist]

        matched_facility_names = [text for text in flat_names_list if facility_map.get(text)]

        if len(matched_facility_names) <= 0:
          continue

        location = Location(latitude=latitude, longitude=longitude)

        # intentionally empty - need to improve crawler
        place_description = ""
        place_type = ""
        place_type = PlaceType(type_name=place_type)

        place = Place(
          place_id=google_id,
          place_name=name,
          place_type=place_type,
          address=address,
          description=place_description,
          location=location)
          
        for facility_name in matched_facility_names:
          place.add_facility(facility_map.get(facility_name))

        try:
          await placeRepository.save(place)
        except DuplicateKeyError:
           ...
   
async def main():
   
    if len(sys.argv) != 3:
        print("Usage: python -m app.scripts.seed_database <lunData path>.json <facilities>.json")

        sys.exit(1)

    facilitiesPath = sys.argv[1]
    lunPath = sys.argv[2]

    print("Facilities path: " + facilitiesPath)
    print("Lun path: " + lunPath)

    await seed_facilities(facilitiesPath)
    await seed_places(lunPath)
   

asyncio.run(main())