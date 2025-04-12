from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import Depends

from app.infrastructure.mongoPlaceRepository import MongoPlaceRepository

MONGO_URI = "mongodb://localhost:27017?directConnection=true"

def get_mongo_client() -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(MONGO_URI)
    return client

def get_database(
        client: AsyncIOMotorClient = Depends(get_mongo_client)) -> AsyncIOMotorDatabase:
    
    return client["MyDb"]


def get_place_repository(
        client: AsyncIOMotorDatabase = Depends(get_database)) -> MongoPlaceRepository:

    return MongoPlaceRepository(client)