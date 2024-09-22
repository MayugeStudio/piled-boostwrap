import typing as tt
from dataclasses import dataclass
from enum import Enum, auto


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
    PUSH_INT = auto()
    PLUS = auto()
    MINUS = auto()
    EQUAL = auto()
    PRINT = auto()


@dataclass(slots=True)
class Token:
    filepath: str
    location: Location
    type: TokenType
    value: tt.Optional[int] = None


class ErrorType(Enum):
    UnknownValue = "UnknownValueError"
