from fastapi import FastAPI, Response, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder

from constants import GOOGLE_API_TOKEN
from structures import Coordinate
from google_api import get_direction

app = FastAPI()

@app.get("/route")
async def api_get_route(origin: Coordinate, destination: Coordinate):
    get_direction(origin, destination)
    return jsonable_encoder(get_direction(origin, destination))


