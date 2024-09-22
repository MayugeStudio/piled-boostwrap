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

class TokenKind(Enum):
    WORD = auto()
    PLUS = auto()
    MINUS = auto()
    PRINT = auto()


@dataclass(slots=True)
class Token:
    filepath: str
    location: Location
    kind: TokenKind
    value: tt.Optional[int] = None


class ErrorKind(Enum):
    UnknownValue = "UnknownValueError"
