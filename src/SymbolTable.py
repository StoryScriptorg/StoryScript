from langEnums import Types
from typing import Any, NoReturn

# This class is used to store variables and function
class SymbolTable:
    def __init__(self):
        self.variable_table: dict = {
            "true": (Types.Boolean, "true"),
            "false": (Types.Boolean, "false"),
        }
        self.function_table: dict = {}

    def copyvalue(self):
        return self.variable_table, self.function_table

    def importdata(self, variableTable, functionTable):
        self.variable_table = variableTable
        self.function_table = functionTable

    def get_all_variable_name(self) -> list[str]:
        """
        Get the name of all variables
        """
        return self.variable_table.keys()

    def GetVariable(self, key: str) -> tuple[Types, Any]:
        """
        Get a variable from key
        """
        return self.variable_table[key]

    def get_variable_type(self, key: str) -> Types:
        """
        Get a Variable type from key
        """
        return self.variable_table[key][0]

    def get_all_function_name(self) -> list[str]:
        """
        Get all function name
        """
        return self.function_table.keys()

    def get_function(self, key: str) -> tuple[list[str], list[str]]:
        """
        Get function from key.
        """
        return self.function_table[key]

    def set_variable(self, key: str, value, vartype: Types) -> NoReturn:
        """
        Set a variable.
        """
        self.variable_table[key] = (vartype, value)

    def setFunction(self, key: str, value: list, arguments: list) -> NoReturn:
        """
        Set a function.
        """
        self.function_table[key] = (arguments, value)

    def DeleteVariable(self, key: str) -> NoReturn:
        """
        Delete a variable from key.
        """
        del self.variable_table[key]

    def DeleteFunction(self, key: str) -> NoReturn:
        """
        Delete a function from key.
        """
        del self.function_table[key]
