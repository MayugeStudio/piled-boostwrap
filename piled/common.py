import typing as tt
from dataclasses import dataclass
from enum import Enum
from enum import auto


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
    GT = auto()
    LT = auto()
    GE = auto()
    LE = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    DO = auto()
    END = auto()
    DUP = auto()
    PRINT = auto()
    MEMORY = auto()
    LOAD = auto()
    STORE = auto()
    SYSCALL3 = auto()


@dataclass(slots=True)
class Token:
    filepath: str
    location: Location
    type: TokenType
    value: tt.Optional[int] = None


class ErrorType(Enum):
    UnknownTokenError = "UnknownTokenError"
