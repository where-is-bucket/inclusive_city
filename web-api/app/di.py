import os

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import Depends

from app.infrastructure.mongoFacilityRepository import MongoFacilityRepository
from app.infrastructure.mongoPlaceRepository import MongoPlaceRepository

MONGO_INITDB_ROOT_USERNAME, MONGO_INITDB_ROOT_PASSWORD = os.getenv("MONGO_INITDB_ROOT_USERNAME"), os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_URI = f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@localhost:27017?directConnection=true"

def get_mongo_client() -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(MONGO_URI)
    return client

def get_database(
        client: AsyncIOMotorClient = Depends(get_mongo_client)) -> AsyncIOMotorDatabase:
    
    return client["MyDb"]


def get_place_repository(
        database: AsyncIOMotorDatabase = Depends(get_database)) -> MongoPlaceRepository:

    return MongoPlaceRepository(database)

def get_facility_repository(
        database: AsyncIOMotorDatabase = Depends(get_database)) -> MongoFacilityRepository:
    
    return MongoFacilityRepository(database)
