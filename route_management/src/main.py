import pprint

from fastapi import FastAPI, Response, Request, HTTPException
from fastapi.encoders import jsonable_encoder

from structures import Coordinate, DirectionsResponse
from google_api import get_direction
from helpers import inject_poi_into_route, get_all_places

app = FastAPI()

@app.get("/route")
async def api_get_route(origin: Coordinate, destination: Coordinate):
    direction = get_direction(origin, destination)
    if len(direction.routes) < 2:
        places = get_all_places()
        for place in places:
            loc = place.location
            poi = Coordinate(lat=loc.latitude, lng=loc.longitude)
            for route in direction.routes:
                new_route = inject_poi_into_route(route, poi)
                direction.routes[0] = new_route
    return jsonable_encoder(get_direction(origin, destination))


