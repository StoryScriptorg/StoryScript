from enum import Enum
from dataclasses import dataclass
from typing import Any


# Constants
LISTDECLARE_KEYW: set = {
    "int[]", "bool[]",
    "float[]", "list[]",
    "dictionary[]", "tuple[]",
    "const", "string[]",
    "dynamic[]",
}
PRIMITIVE_TYPE: set = {
    "var", "int",
    "bool", "float",
    "list", "dictionary",
    "tuple", "const",
    "string", "dynamic",
    "Action", "void"
}
# All Keywords
BASE_KEYWORDS: set = {
    "if", "else",
    "override",
    "func", "end",
    "throw", "string",
    "typeof", "del",
    "namespace",
    "#define",
    "loopfor",
    "switch", "?",
    "void", "while",
    "lambda", "new",
    "null", "import"
}
BASE_KEYWORDS.update(LISTDECLARE_KEYW)
BASE_KEYWORDS.update(PRIMITIVE_TYPE)
MODULES: dict = {
    "tkinter": "modules.tkinter"
}

# Error messages
paren_needed: str = "InvalidSyntax: Parenthesis is needed after a function name"
close_paren_needed: str = "InvalidSyntax: Parenthesis is needed after an Argument input"
invalid_value: str = "InvalidValue: Invalid value"
mismatch_type: str = "InvalidValue: Value doesn't match variable type."
not_enough_args_for_import_statement: str = "NotDefinedException: Not enough arguments for import statement."


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


class Types(Enum): # data types
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

class Signal(Enum):
    PRINT = 0
    NONE = 1


@dataclass
class Array:
    dtype: Types
    shape: list # real type: list[int]
    data: Any

    def __repr__(self):
        return str(self.data)


def convert_args_to_readable_format(args: list):
    def convert(arg):
        arg[0] = arg[0].value
        return f"{arg[0]} {arg[1]}"
    return list(map(convert, args))


@dataclass
class LambdaExpr:
    arguments: list
    return_type: Types
    function_body: str
    
    def __repr__(self):
        return f"lambda {self.return_type.value} {convert_args_to_readable_format(self.arguments)} => {self.function_body}"

@dataclass
class PythonFunctionObject:
    return_type: Types
    name: str
    arguments: tuple
    function_body: Any

    def __repr__(self):
        return f"{self.return_type} {self.name}{self.arguments}"

class ConditionType(Enum):
    And = 0
    Or = 1
    Single = 2
