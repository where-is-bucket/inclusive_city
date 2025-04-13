import asyncio
import json
import os
import sys
from urllib.parse import urlsplit

import requests

from motor.motor_asyncio import AsyncIOMotorClient

from pymongo.errors import DuplicateKeyError

from app.domain.disabilityTypes import DisabilityType
from app.domain.facility import Facility
from app.domain.location import Location
from app.domain.place import Place
from app.domain.placeType import PlaceType
from app.infrastructure.mongoFacilityRepository import MongoFacilityRepository
from app.infrastructure.mongoPlaceRepository import MongoPlaceRepository

MONGO_URI = os.getenv("MONGO_CONNECTION") or f"mongodb://localhost:27017?directConnection=true"
#MONGO_URI = f"mongodb://localhost:27017?directConnection=true"

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

async def seed_places(path, api_key):
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
        
        google_photo_url = item.get('photo_url')

        if google_photo_url: 
           google_photo_url = urlsplit(google_photo_url)._replace(query="").geturl()

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

        place_description = ''
        place_types = []

        # enrich additional data
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={google_id}&key={api_key}"
        
        response = requests.get(url)
        data = response.json()
        if data.get("status") == "OK":
            
          result = data["result"]

          if result:          
            place_types = result.get("types", [])
            place_description = result.get("editorial_summary", {}).get("overview", '')

        
        place = Place(
          place_id=google_id,
          place_name=name,
          place_types=place_types,
          address=address,
          description=place_description,
          google_photo_url=google_photo_url,
          location=location)
          
        for facility_name in matched_facility_names:
          place.add_facility(facility_map.get(facility_name))

        try:
          await placeRepository.save(place)
        except DuplicateKeyError:
           ...

async def main():
   
    if len(sys.argv) != 4:
        print("Usage: python -m app.scripts.seed_database <lunData path>.json <facilities>.json <api_key>")

        sys.exit(1)

    facilitiesPath = sys.argv[1]
    lunPath = sys.argv[2]
    apiKey = sys.argv[3]

    print("Facilities path: " + facilitiesPath)
    print("Lun path: " + lunPath)
    print(MONGO_URI)


    current_facilities = await database["Facilities"].count_documents({})

    if current_facilities == 0:
      print('Seeding facilities')
      await seed_facilities(facilitiesPath)
    else:
       print('Skip facilities seeding')

    current_places = await database["Places"].count_documents({})

    if current_places == 0:
      print('Seeding places')
      await seed_places(lunPath, apiKey)
    else:
       print('Skip places seeding')

   

asyncio.run(main())