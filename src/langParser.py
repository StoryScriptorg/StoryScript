from string import ascii_letters, digits
from langEnums import Types, Exceptions, ConditionType, Array, LambdaExpr
from mathParser.mathProcessor import process as processmath
import mathParser.values
import executor
from typing import Any


# Constants
KEYWORDS: set = {
    "if",
    "else",
    "var",
    "int",
    "bool",
    "float",
    "list",
    "dictionary",
    "tuple",
    "const",
    "override",
    "func",
    "end",
    "print",
    "input",
    "throw",
    "string",
    "typeof",
    "del",
    "namespace",
    "?",
    "null",
    "true",
    "false"
}
COMP_OPERATOR: set = {">", "<", "==", "!=", ">=", "<="}


class Parser:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    @staticmethod
    def convert_to_python_native_type(valtype, value) -> Any:
        """
        Returns a Python version of the value provided to a Type specified.
        [PARAMETER] valtype: Target output type
        [PARAMETER] value: The input value that will be converted.
        [RETURNS]
        a Converted value,
        Else None If the type is not support yet by the Converter.
        """
        if valtype == Types.Integer:
            return int(value)
        if valtype == Types.Float:
            if isinstance(value, mathParser.values.Number):
                value = value.value
            return float(value)
        if valtype == Types.String:
            return str(value[1:-1])
        if valtype == Types.Boolean:
            if value == "true":
                return True
            if value == "false":
                return False

    @staticmethod
    def parse_type_from_value(value) -> Types:
        if isinstance(value, Array):
            return Types.Array
        if isinstance(value, LambdaExpr):
            return Types.Action
        if value in {None, "null"}:
            return Types.Void
        if not isinstance(value, str):
            value = str(value)
        if value in ("true", "false"):
            return Types.Boolean
        # Unimplemented types
        # if value.startswith("new List"):
        #     return Types.List
        # if value.startswith("new Dictionary"):
        #     return Types.Dictionary
        # if value.startswith("new Tuple"):
        #     return Types.Tuple
        if value.startswith("new Dynamic"):
            return Types.Dynamic

        is_float = executor.check_is_float(value)
        if value.startswith('"') or value.endswith('"'):
            return Types.String

        if is_float:
            return Types.Float
        if not is_float:
            return Types.Integer

    @staticmethod
    def parse_type_string(string) -> Types:
        if string == "bool":
            return Types.Boolean
        if string == "int":
            return Types.Integer
        if string == "float":
            return Types.Float
        if string == "list":
            return Types.List
        if string == "dictionary":
            return Types.Dictionary
        if string == "tuple":
            return Types.Tuple
        if string == "dynamic":
            return Types.Dynamic
        if string == "string":
            return Types.String
        if string == "any":
            return Types.Any
        if string == "void":
            return Types.Void
        if string == "Action":
            return Types.Action
        return Exceptions.InvalidSyntax

    @staticmethod
    def check_naming_violation(name) -> bool:
        """Returns If the variable naming valid or not"""
        if not isinstance(name, str):
            name = str(name)
        if name in KEYWORDS:
            return False
        if name[0] in digits:
            return False
        return True

    def parse_conditions(self, conditionslist, analyse_command_method) -> bool:
        allexpr_result = []
        for i in conditionslist:
            expr_result = []
            current_condition_type = ConditionType.Single
            for j in i:
                if j and isinstance(j, list):
                    result, error = self.parse_condition_expression(j, analyse_command_method)
                    if error:
                        return result, error
                    expr_result.append(result)
                elif isinstance(j, ConditionType):
                    current_condition_type = j
            if current_condition_type == ConditionType.And:
                allexpr_result.append(all(expr_result))
            elif current_condition_type == ConditionType.Single:
                allexpr_result.append(expr_result[0])
            elif current_condition_type == ConditionType.Or:
                allexpr_result.append(any(expr_result))

        return all(allexpr_result), None

    def parse_condition_expression(self, expr, analyse_command_method) -> tuple:
        """Parse If the condition is True or False"""
        # [:operator_index] = Accessing a Message before the operator
        # [operator_index + 1:] = Accessing a Message after the operator
        operator_index = 0
        for i in expr:
            if i in COMP_OPERATOR:
                break
            operator_index += 1
        resl, error = analyse_command_method(
            expr[:operator_index]
        )  # Analyse the message on the left
        if error:
            return resl, error

        resr, error = analyse_command_method(
            expr[operator_index + 1 :]
        )  # Analyse the message on the right
        if error:
            return resr, error

        # Type conversion
        restype = self.parse_type_from_value(resl)
        resl = self.convert_to_python_native_type(restype, resl)
        if resr:
            restype = self.parse_type_from_value(resr)
            resr = self.convert_to_python_native_type(restype, resr)

        if isinstance(resl, str):
            if resl.startswith('"') and resl.endswith('"'):
                resl = resl[1:-1]
            if resr.startswith('"') and resr.endswith('"'):
                resr = resr[1:-1]

        try:
            if expr[operator_index] == "==":  # If the operator was ==
                if resl == resr:
                    return True, None
            elif expr[operator_index] == ">":  # If the operator was >
                if resl > resr:
                    return True, None
            elif expr[operator_index] == "<":  # If the operator was <
                if resl < resr:
                    return True, None
            elif expr[operator_index] == "!=":  # If the operator was !=
                if resl != resr:
                    return True, None
            elif expr[operator_index] == ">=":  # If the operator was >=
                if resl >= resr:
                    return True, None
            elif expr[operator_index] == "<=":  # If the operator was <=
                if resl <= resr:
                    return True, None
            else:
                return "Unknown comparison operator."
        except IndexError:
            if resl:
                return True, None

        return False, None

    @staticmethod
    def parse_condition_list(expr) -> list:
        """Separate expressions into a list of conditions"""
        conditionslist: list = []  # List of conditions
        conditions: list = []  # List of condition
        condition: list = []  # Condition
        current_condition_type = ConditionType.Single  # Current condition type
        for i in expr:
            if i == "and":
                if current_condition_type != ConditionType.Single:
                    conditions.append(condition)
                    conditions.append(current_condition_type)
                    conditionslist.append(conditions)
                    conditions = []
                    condition = []
                conditions.append(condition)
                condition = []
                current_condition_type = ConditionType.And
                continue
            if i == "or":
                if current_condition_type != ConditionType.Single:
                    conditions.append(condition)
                    conditions.append(current_condition_type)
                    conditionslist.append(conditions)
                    conditions = []
                    condition = []
                conditions.append(condition)
                condition = []
                current_condition_type = ConditionType.Or
                continue
            if i == "then":
                conditions.append(condition)
                conditions.append(current_condition_type)
                conditionslist.append(conditions)
                conditions = []
                condition = []
                break
            condition.append(i)
        return conditionslist

    @staticmethod
    def throw_keyword(tc: list, analyse_command) -> tuple:
        # Throw keyword. "throw [Exception] [Description]"
        errstr = ""
        errenum = None
        description = "No Description provided"

        if tc[1] == "InvalidSyntax":
            errstr = "InvalidSyntax"
            errenum = Exceptions.InvalidSyntax
        elif tc[1] == "AlreadyDefined":
            errstr = "AlreadyDefined"
            errenum = Exceptions.AlreadyDefined
        elif tc[1] == "NotImplementedException":
            errstr = "NotImplementedException"
            errenum = Exceptions.NotImplementedException
        elif tc[1] == "NotDefinedException":
            errstr = "NotDefinedException"
            errenum = Exceptions.NotDefinedException
        elif tc[1] == "GeneralException":
            errstr = "GeneralException"
            errenum = Exceptions.GeneralException
        elif tc[1] == "DivideByZeroException":
            errstr = "DivideByZeroException"
            description = "You cannot divide numbers with 0"
            errenum = Exceptions.DivideByZeroException
        elif tc[1] == "InvalidValue":
            errstr = "InvalidValue"
            errenum = Exceptions.InvalidValue
        elif tc[1] == "InvalidTypeException":
            errstr = "InvalidTypeException"
            errenum = Exceptions.InvalidTypeException
        elif tc[1] == "InvalidOperatorException":
            errstr = "InvalidOperatorException"
            errenum = Exceptions.InvalidOperatorException
        else:
            return (
                "InvalidValue: The Exception entered is not defined",
                Exceptions.InvalidValue,
            )

        try:
            new_description, error = analyse_command(tc[2:])
            if error:
                return new_description, error
            if new_description is not None:
                description = new_description
                if isinstance(description, str) and description.startswith('"') \
                    and description.endswith('"'):
                    description = description[1:-1]
        except IndexError:
            pass

        return f"{errstr}: {description}", errenum

    @staticmethod
    def parse_argument(argumentstring, seperator: str = " ") -> str:
        if isinstance(argumentstring, list):
            argumentstring = seperator.join(argumentstring)
        argument = ""
        in_paren = 0
        for i in argumentstring:
            if i == "(":
                in_paren += 1
                if in_paren == 1:
                    continue
            if i == ")":
                in_paren -= 1
                if in_paren == 0:
                    break
            if in_paren > 0:
                argument += i
        return argument

    @staticmethod
    def split_arguments(argumentstring: str) -> list:
        in_string = False
        args = []
        argstring = ""
        for i in argumentstring:
            if i in {'"', "'"}:
                in_string = not in_string
            elif i == "," and not in_string:
                args.append(argstring)
                argstring = ""
                continue
            argstring += i
        args.append(argstring)
        return args

    def parse_expression(self, command, keep_float=False) -> tuple:
        try:
            res = processmath(command, self.symbol_table)[0]
            if isinstance(res.value, str):
                return res.value, None
            if keep_float:
                return float(res.value), None
            try:
                if not executor.check_is_float(res.value):
                    return int(res.value), None
            except ValueError:
                pass
            return res, None
        except SyntaxError as e:
            return f"InvalidSyntax: {e}", Exceptions.InvalidSyntax
        except TypeError as e:
            return f"InvalidTypeException: {e}", Exceptions.InvalidTypeException
        except ZeroDivisionError:
            return (
                "DivideByZeroException: You cannot divide numbers with 0",
                Exceptions.DivideByZeroException,
            )
        except NameError as e:
            return f"NotDefinedException: {e}", Exceptions.NotDefinedException
