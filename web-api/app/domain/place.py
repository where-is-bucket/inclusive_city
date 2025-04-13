from typing import List, Optional

from pydantic import BaseModel
from app.domain.facility import Facility
from app.domain.location import Location
from app.domain.placeType import PlaceType
from app.domain.review import Review

class Place(BaseModel):
    place_id: Optional[str] = None
    google_id: str
    place_name: str
    place_type: PlaceType
    address: str
    description: str
    location: Location
    accessibility_rate: float = 0
    reviews: List[Review] = []
    facilities: List[Facility] = []

    def add_review(self, review: Review) -> None:
        self.reviews.append(review)

    def add_facility(self, facility: Facility):
        
        if any(x.facility_id == facility.facility_id for x in self.facilities):
            raise FacilityAlreadyExistException(facility)

        self.facilities.append(facility)

class FacilityAlreadyExistException(Exception):
    def __init__(self, accessibility: Facility):
        self.accessibility = accessibility

        super().__init__(f"Facility feature '{accessibility.name}' already exists.")
