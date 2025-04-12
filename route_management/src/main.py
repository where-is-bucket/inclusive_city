import pprint

from fastapi import FastAPI, Response, Request, HTTPException
from fastapi.encoders import jsonable_encoder

from structures import Coordinate, DirectionsResponse
from google_api import get_direction
from helpers import inject_poi_into_route

app = FastAPI()

@app.get("/route")
async def api_get_route(origin: Coordinate, destination: Coordinate):
    direction = get_direction(origin, destination)
    poi = Coordinate(lat=50.4501, lng=30.5234) # in the next version we will take it from the MongoDB
    if len(direction.routes) < 2:
        for route in direction.routes:
            new_route = inject_poi_into_route(route, poi)
            direction.routes[0] = new_route
    return jsonable_encoder(get_direction(origin, destination))


