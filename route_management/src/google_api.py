import requests
import pprint

from constants import GOOGLE_API_TOKEN, DIRECTION_GOOGLE_API_URL
from structures import Coordinate, DirectionsResponse

def get_direction(origin: Coordinate, destination: Coordinate):
    params = {
        "origin": f"{origin.lat},{origin.lng}",
        "destination": f"{destination.lat},{destination.lng}",
        "key": GOOGLE_API_TOKEN
    }
    response = requests.get(DIRECTION_GOOGLE_API_URL, params=params, timeout=3)
    pprint.pprint(DirectionsResponse(**response.json()))
    return response.json()