import typing as tt
from dataclasses import dataclass
from enum import Enum, auto

from piled.common import Token, TokenType


class IRType(Enum):
    PUSH_INT = auto()
    PLUS = auto()
    MINUS = auto()
    PRINT = auto()


@dataclass(slots=True)
class IR:
    type: IRType
    value: tt.Optional[int] = None


def build_IR_from_token(token: Token) -> IR:
    if token.type == TokenType.PLUS:
        return IR(IRType.PLUS)
    elif token.type == TokenType.MINUS:
        return IR(IRType.MINUS)
    elif token.type == TokenType.PRINT:
        return IR(IRType.PRINT)
    elif token.type == TokenType.WORD:
        return IR(IRType.PUSH_INT, value=token.value)
    else:
        assert "unreachable"
