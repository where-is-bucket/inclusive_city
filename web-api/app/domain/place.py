from typing import List, Optional

from pydantic import BaseModel
from app.domain.facility import Facility
from app.domain.location import Location
from app.domain.placeType import PlaceType
from app.domain.review import Review

class Place(BaseModel):
    place_id: str
    place_name: str
    place_types: List[str] = [],
    address: str
    description: str
    google_photo_url: Optional[str]
    location: Location
    accessibility_rate: float = 0
    reviews: List[Review] = []
    facilities: List[Facility] = []

    def add_review(self, review: Review) -> None:
        self.reviews.append(review)

    def add_facility(self, addedFacility: Facility):
        
        if any(x.facility_id == addedFacility.facility_id for x in self.facilities):
            return

        self.facilities.append(addedFacility)

    def remove_facility(self, removedFacility: Facility):

        self.facilities = [f for f in self.facilities if f.facility_id != removedFacility.facility_id]
