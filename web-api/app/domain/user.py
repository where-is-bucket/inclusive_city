from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    is_special: bool