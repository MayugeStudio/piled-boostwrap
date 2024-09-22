from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Location:
    row: int
    col: int

@dataclass(slots=True)
class Word:
    filepath: str
    location: Location
    value: str
