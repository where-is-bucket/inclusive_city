from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass
@dataclass_json
class Facility:
    facility_id: int
    disability_type :str
    name: str
    description: str
