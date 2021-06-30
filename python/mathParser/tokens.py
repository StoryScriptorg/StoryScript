from enum import Enum
from dataclasses import dataclass
from typing import Any


class TokenType(Enum):
    NUMBER = 0
    PLUS = 1
    MINUS = 2
    MULTIPLY = 3
    DIVIDE = 4
    MODULO = 5
    LPAREN = 6
    RPAREN = 7
    STRING = 8
    POWER = 9


@dataclass
class Token:
    type: TokenType
    value: Any = None

    def __repr__(self):
        return self.type.name + (f":{self.value}" if self.value is not None else "")
