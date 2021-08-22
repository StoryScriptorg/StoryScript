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
    InvalidIndexException = 108
    InvalidOperatorException = 109


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
    Void = "void"
    Action = "action" # Lambda expression type


@dataclass
class Array:
    dtype: Types
    shape: list[int]
    data: Any

    def __repr__(self):
        return str(self.data)


@dataclass
class LambdaExpr:
    arguments: list
    return_type: Types
    function_body: str

    @staticmethod
    def convert_args_to_readable_format(args: list):
        def convert(arg):
            arg[0] = arg[0].value
            return f"{arg[0]} {arg[1]}"
        return list(map(convert, args))
    
    def __repr__(self):
        return f"lambda {self.return_type.value} {self.convert_args_to_readable_format(self.arguments)} => {self.function_body}"


class ConditionType(Enum):
    And = 0
    Or = 1
    Single = 2
