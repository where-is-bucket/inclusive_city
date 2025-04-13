from typing import List
from geopy.distance import distance as geodistance
from polyline import encode as polyline_encode
import requests
from pprint import pprint
import json

from structures import DirectionsResponse, Route, Leg, Step, Coordinate, Place
from constants import webapi_url


def inject_poi_into_route(route: Route, poi: Coordinate, max_distance_m: float = 0.01) -> Route:
    new_legs = []
    injected = False

    for leg in route.legs:
        new_steps: List[Step] = []

        for step in leg.steps:
            dist_from_poi = geodistance(
                (step.end_location.lat, step.end_location.lng),
                (poi.lat, poi.lng)
            ).meters
            dist_to_poi = geodistance(
                (step.start_location.lat, step.start_location.lng),
                (poi.lat, poi.lng)
            ).meters

            if not injected and dist_to_poi <= max_distance_m:
                step_to_poi = Step(
                    start_location=step.start_location,
                    end_location=poi,
                    polyline={"points": polyline_encode([
                        [step.start_location.lat, step.start_location.lng],
                        [poi.lat, poi.lng]
                    ])},
                    html_instructions="Detour to priority location",
                    distance={"value": int(dist_to_poi)},
                    duration={"value": int(dist_to_poi)/0.2},
                    travel_mode="WALKING"
                )

                step_from_poi = Step(
                    start_location=poi,
                    end_location=step.end_location,
                    polyline={"points": polyline_encode([
                        [poi.lat, poi.lng],
                        [step.end_location.lat, step.end_location.lng]
                    ])},
                    html_instructions="Continue to next point",
                    distance={"value": int(dist_from_poi)},
                    duration={"value": int(dist_from_poi)/0.2},
                    travel_mode="WALKING"
                )

                new_steps.extend([step_to_poi, step_from_poi])
                injected = True
            else:
                new_steps.append(step)

        leg.steps = new_steps
        new_legs.append(leg)

    route.legs = new_legs
    return route

def get_all_places():
    places: List[Place] = [Place(**p) for p in requests.get(f"http://{webapi_url}/api/v1/places", timeout=3).json()]
    return places