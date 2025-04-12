import os

import requests

from constants import GOOGLE_API_TOKEN, DIRECTION_GOOGLE_API_URL
from structures import Coordinate, DirectionsResponse

def get_direction(origin: Coordinate, destination: Coordinate) -> DirectionsResponse:
    params = {
        "origin": f"{origin.lat},{origin.lng}",
        "destination": f"{destination.lat},{destination.lng}",
        "units": "metric",
        "mode": "walking",
        "key": GOOGLE_API_TOKEN
    }
    response = requests.get(os.path.join(DIRECTION_GOOGLE_API_URL, "json"), params=params, timeout=3)
    direct_resp = DirectionsResponse(**response.json())
    return direct_resp

