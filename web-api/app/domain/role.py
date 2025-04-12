# Value object representing user role
from dataclasses import dataclass


@dataclass
class Role:
    
    def __init__(self, name: str):
        self._name = name;

    @property
    def name(self):
        return self._name;