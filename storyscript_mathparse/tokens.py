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
    BITWISE_OR = 10
    BITWISE_AND = 11
    BITWISE_LS = 12  # Bit shifting (left) (<<)
    BITWISE_RS = 13  # Bit shifting (right) (>>)
    BITWISE_XOR = 14
    BITWISE_NOT = 15
    INCREMENT_SYMBOL = 16 # variable++
    DECREMENT_SYMBOL = 17 # variable--


@dataclass
class Token:
    type: TokenType
    value: Any = None

    def __repr__(self):
        return self.type.name + (f":{self.value}" if self.value is not None else "")
