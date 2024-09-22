from dataclasses import dataclass
from enum import Enum, auto
import typing as tt

@dataclass(frozen=True, slots=True)
class Location:
    row: int
    col: int

@dataclass(slots=True)
class Word:
    filepath: str
    location: Location
    value: str

class TokenType(Enum):
    WORD = auto()
    PLUS = auto()
    MINUS = auto()
    PRINT = auto()


@dataclass(slots=True)
class Token:
    filepath: str
    location: Location
    type: TokenType
    value: tt.Optional[int] = None


class ErrorType(Enum):
    UnknownValue = "UnknownValueError"
