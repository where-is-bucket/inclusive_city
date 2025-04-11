from typing import Optional, List

from pydantic import BaseModel, Field


class Coordinate(BaseModel):
    lat: float
    lng: float
    class Config:
        schema_extra = {
            "examples":{
                "lat": 48.16,
                "lng": 24.500278
            }
        }


class Step(BaseModel):
    distance: dict
    duration: dict
    end_location: Coordinate
    start_location: Coordinate
    html_instructions: str
    travel_mode: str
    polyline: dict

class Leg(BaseModel):
    distance: dict
    duration: dict
    end_address: str
    start_address: str
    end_location: Coordinate
    start_location: Coordinate
    steps: List[Step]

class Bounds(BaseModel):
    northeast: Coordinate
    southwest: Coordinate

class OverviewPolyline(BaseModel):
    points: str

class Route(BaseModel):
    bounds: Bounds
    summary: str
    legs: List[Leg]
    overview_polyline: OverviewPolyline
    warnings: List[str]
    waypoint_order: Optional[List[int]] = []

class DirectionsResponse(BaseModel):
    geocoded_waypoints: Optional[List[dict]] = []
    routes: List[Route]
    status: str
    class Config:
        schema_extra = {
            "examples":
                {
                    {
                        "geocoded_waypoints": [
                            {"geocoder_status": "OK", "place_id": "ChIJ7XJ9eyn9NkcRfrI6MDzJud4", "types": ["route"]},
                            {"geocoder_status": "OK", "place_id": "ChIJ7XJ9eyn9NkcRfrI6MDzJud4", "types": ["route"]}],
                        "routes": [{"bounds": {"northeast": {"lat": 48.1622485, "lng": 24.4906349},
                                               "southwest": {"lat": 48.1622485, "lng": 24.4906349}},
                                    "copyrights": "Powered by Google, ©2025 Google", "legs": [
                                {"distance": {"text": "1 m", "value": 0}, "duration": {"text": "1 min", "value": 0},
                                 "end_address": "Ekoloho-Piznavalʹna Stezhka \"Na H. Hoverla\", Ivano-Frankivs'ka oblast, Ukraine",
                                 "end_location": {"lat": 48.1622485, "lng": 24.4906349},
                                 "start_address": "Ekoloho-Piznavalʹna Stezhka \"Na H. Hoverla\", Ivano-Frankivs'ka oblast, Ukraine",
                                 "start_location": {"lat": 48.1622485, "lng": 24.4906349}, "steps": [
                                    {"distance": {"text": "1 m", "value": 0}, "duration": {"text": "1 min", "value": 0},
                                     "end_location": {"lat": 48.1622485, "lng": 24.4906349}, "html_instructions": "Head",
                                     "polyline": {"points": "au}dHmintC"},
                                     "start_location": {"lat": 48.1622485, "lng": 24.4906349}, "travel_mode": "DRIVING"}],
                                 "traffic_speed_entry": [], "via_waypoint": []}],
                                    "overview_polyline": {"points": "au}dHmintC"}, "summary": "", "warnings": [],
                                    "waypoint_order": []}], "status": "OK"}
                }

        }