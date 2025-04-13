from typing import List, Optional
import uuid
from pydantic import BaseModel, ConfigDict

from app.domain.disabilityTypes import DisabilityType

class Facility(BaseModel):
    facility_id: str
    disability_types: List[DisabilityType]
    descriptive_name: str

    @staticmethod
    def create(disability_types: List[DisabilityType], descriptive_name: str):
        return Facility(
            facility_id=str(uuid.uuid4()),
            disability_types=disability_types,
            descriptive_name=descriptive_name)
    

    model_config = ConfigDict(use_enum_values=True)
