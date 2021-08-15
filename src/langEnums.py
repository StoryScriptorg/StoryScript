from enum import Enum
from dataclasses import dataclass
from typing import Any


class Exceptions(Enum):
    InvalidSyntax = 100
    AlreadyDefined = 101
    NotImplementedException = 102
    NotDefinedException = 103
    GeneralException = 104
    DivideByZeroException = 105
    InvalidValue = 106
    InvalidTypeException = 107


class Types(Enum):
    Boolean = "bool"
    Integer = "int"
    Float = "float"
    List = "list"
    Dictionary = "dictionary"
    Tuple = "tuple"
    Dynamic = "dynamic"
    String = "string"
    Any = "any"
    Array = "array"


@dataclass
class Array:
    dtype: Types
    shape: list[int]
    data: Any

    def __repr__(self):
        return str(self.data)


class ConditionType(Enum):
    And = 0
    Or = 1
    Single = 2
