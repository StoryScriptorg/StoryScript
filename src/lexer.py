import numpy as np
from langEnums import Exceptions, Types, Array
from typing import Any, NoReturn
from langParser import Parser
# from cachelogger import CacheLogger
from SymbolTable import SymbolTable
import mathParser.values
import executor

# Constants
LISTDECLARE_KEYW: set = {
    "int[]",
    "bool[]",
    "float[]",
    "list[]",
    "dictionary[]",
    "tuple[]",
    "const",
    "string[]",
    "dynamic[]",
}
PRIMITIVE_TYPE: set = {
    "var",
    "int",
    "bool",
    "float",
    "list",
    "dictionary",
    "tuple",
    "const",
    "string",
    "dynamic",
}
# All Keywords
BASE_KEYWORDS: set = {
    "if",
    "else",
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
    "#define",
    "loopfor",
    "switch",
    "exit",
    "?",
    "void",
    "while",
}
BASE_KEYWORDS.update(LISTDECLARE_KEYW)
BASE_KEYWORDS.update(PRIMITIVE_TYPE)

# Error messages
paren_needed: str = "InvalidSyntax: Parenthesis is needed after a function name"
close_paren_needed: str = "InvalidSyntax: Parenthesis is needed after an Argument input"
invalid_value = "InvalidValue: Invalid value"
mismatch_type = "InvalidValue: Value doesn't match variable type."


class Lexer:
    def __init__(
        self,
        symbol_table: SymbolTable,
        parser: Parser = None,
        build_cache: bool = False,
    ) -> NoReturn:
        self.symbol_table: SymbolTable = symbol_table
        self.parser: Parser = parser
        self.build_cache: bool = build_cache

        if parser is None:
            self.parser: Parser = Parser(symbol_table)

    def throw_keyword(self, tc: list) -> tuple[str, Exceptions]:
        # Throw keyword. "throw [Exception] [Description]"
        def get_description():
            msg = ""
            for i in tc[2:]:
                if i.startswith('"'):
                    i = i[1:]
                if i.endswith('"'):
                    i = i[:-1]
                    msg += i + " "
                    break
                msg += i + " "
            msg = msg[:-1]
            return self.parser.parse_escape_character(msg)

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
        else:
            return (
                "InvalidValue: The Exception entered is not defined",
                Exceptions.InvalidValue,
            )

        try:
            if tc[2:]:
                description = get_description()
        except IndexError:
            pass

        return f"{errstr}: {description}", errenum

    def variable_setting(self, tc: list) -> tuple[Any, Any]:
        all_variable_name = self.symbol_table.get_all_variable_name()

        if tc[1] == "=":  # Set operator
            value = " ".join(tc[2:])
            if value.startswith("new Dynamic ("):
                value = value[13:-1]
            res, error = self.analyse_command(value.split())
            if error:
                return res, error
            value = ""

            for i in tc[2:]:
                value += i + " "
            value = value[:-1]

            valtype = self.parser.parse_type_from_value(res)
            if valtype == Exceptions.InvalidSyntax:
                return invalid_value, Exceptions.InvalidValue
            vartype = self.symbol_table.GetVariableType(tc[0])
            # Check if Value Type matches Variable type
            if valtype != vartype:
                return mismatch_type, Exceptions.InvalidValue
            res = self.parser.parse_escape_character(res)
            if res in all_variable_name:
                res = (self.symbol_table.GetVariable(res))[1]
            self.symbol_table.set_variable(tc[0], res, vartype)
            return None, None
        if tc[1] == "+=":  # Add & Set operator
            operator = "+"
        elif tc[1] == "-=":  # Subtract & Set operator
            operator = "-"
        elif tc[1] == "*=":  # Multiply & Set operator
            operator = "*"
        elif tc[1] == "/=":  # Divide & Set operator
            operator = "/"
        elif tc[1] == "%=":  # Modulo Operaion & Set operator
            operator = "%"
        else:
            res, error = self.parser.parse_expression(tc[0:])
            return res, error

        vartype = self.symbol_table.GetVariableType(tc[0])
        keepFloat = False
        if vartype == Types.Float:
            keepFloat = True
        res, error = self.analyse_command(tc[2:])
        if error:
            return res, error
        res, error = self.parser.parse_expression(
            [tc[0], operator, str(res)], keepFloat
        )
        value = ""
        try:
            if tc[2] in all_variable_name:
                tc[2] = (self.symbol_table.GetVariable(tc[2]))[1]
            if tc[4] in all_variable_name:
                tc[4] = (self.symbol_table.GetVariable(tc[4]))[1]
        except IndexError:
            pass

        value = " ".join(tc[2:])

        valtype = self.parser.parse_type_from_value(res)
        if valtype == Exceptions.InvalidSyntax:
            return invalid_value, Exceptions.InvalidValue

        # Check if Value Type matches Variable type
        if valtype != vartype:
            return mismatch_type, Exceptions.InvalidValue
        res = self.parser.parse_escape_character(res)
        self.symbol_table.set_variable(tc[0], res, vartype)
        return None, None

    def if_else_statement(self, tc: list) -> tuple[type(None), type(None)]:
        runCode, error = self.parser.parse_conditions(
            self.parser.parse_condition_list(tc[1:]), self.analyse_command
        )
        if error:
            return runCode, error

        is_in_code_block = False
        is_in_else_block = False
        have_passed_then_keyword = False
        ifstatement = {"if": [], "else": []}
        commands = []
        command = []
        endkeywordcount = 0  # All "end" keyword in the expression
        endkeywordpassed = 0  # All "end" keyword passed
        elsekeywordcount = 0  # All "else" keyword in the expression
        elsekeywordpassed = 0  # All "else" keyword passed
        for i in tc[2:]:
            if i == "end":
                endkeywordcount += 1
            elif i == "else":
                elsekeywordcount += 1
        for i in tc:
            if not have_passed_then_keyword and i == "then":
                is_in_code_block = True
                have_passed_then_keyword = True
                continue
            if is_in_code_block:
                if i == "&&":
                    commands.append(command)
                    command = []
                    continue
                if i == "end":
                    endkeywordpassed += 1
                    if endkeywordcount == endkeywordpassed:
                        commands.append(command)
                        command = []
                        if is_in_else_block:
                            ifstatement["else"] = commands
                        else:
                            ifstatement["if"] = commands
                        is_in_else_block = False
                        is_in_code_block = False
                        continue
                if i == "else":
                    elsekeywordpassed += 1
                    if (
                        elsekeywordcount == elsekeywordpassed
                        and endkeywordpassed + 1 == endkeywordcount
                    ):
                        commands.append(command)
                        command = []
                        ifstatement["if"] = commands
                        commands = []
                        is_in_else_block = True
                        continue
                command.append(i)

        # Run the code if the condition is true
        if runCode:
            for i in ifstatement["if"]:
                res, error = self.analyse_command(i)
                if error:
                    return res, error
                if res is not None:
                    print(res)
        else:
            # Iterate through commands
            for i in ifstatement["else"]:
                res, error = self.analyse_command(i)
                if error:
                    return res, error
                if res is not None:
                    print(res)

        return None, None

    def loopfor_statement(self, tc: list) -> tuple[type(None), type(None)]:
        try:
            commands = []  # list of commands
            command = []
            endkeywordcount = 0  # All "end" keyword in the expression
            endkeywordpassed = 0  # All "end" keyword passed
            for i in tc[2:]:
                if i == "end":
                    endkeywordcount += 1
            for i in tc[2:]:
                if i == "&&":
                    commands.append(command)
                    command = []
                    continue
                if i == "end":
                    endkeywordpassed += 1
                    if endkeywordcount == endkeywordpassed:
                        commands.append(command)
                        command = []
                        break
                command.append(i)
            vartable, functable = self.symbol_table.copyvalue()
            scoped_variable_table = SymbolTable()
            scoped_variable_table.importdata(vartable, functable)
            commandlexer = Lexer(scoped_variable_table)
            index = 0
            if tc[1].endswith(":"):
                tc[1] = tc[1][:-1]
            times, error = self.analyse_command(tc[1])
            if error:
                return times, error
            while index < times:
                scoped_variable_table = SymbolTable()
                commandlexer.symbol_table = scoped_variable_table
                for i in commands:
                    res, error = commandlexer.analyse_command(i)
                    if error:
                        return res, error
                    if res is not None:
                        print(res)
                index += 1
            return None, None
        except ValueError:
            return (
                "InvalidValue: Count must be an Integer. (Whole number)",
                Exceptions.InvalidValue,
            )

    def switch_case_statement(self, tc: list) -> tuple[type(None), type(None)]:
        all_variable_name = self.symbol_table.get_all_variable_name()
        cases = {}
        case = []
        command = []
        is_in_case_block = False
        is_after_case_keyword = False
        current_case_key = None
        for i in tc[2:]:
            if i == "case":
                is_after_case_keyword = True
                continue
            if is_after_case_keyword:
                outkey = i
                if outkey.endswith(":"):
                    outkey = outkey[:-1]
                current_case_key = outkey
                is_after_case_keyword = False
                is_in_case_block = True
                continue
            if is_in_case_block:
                if i == "&&":
                    case.append(command)
                    command = []
                    continue
                if i == "break":
                    case.append(command)
                    cases[current_case_key] = case
                    command = []
                    case = []
                    is_in_case_block = False
                    continue
                command.append(i)
            if i == "end":
                break

        if tc[1] in all_variable_name:
            tc[1] = self.symbol_table.GetVariable(tc[1])[1]

        scopedVariableTable = SymbolTable()
        vartable, functable = self.symbol_table.copyvalue()
        scopedVariableTable.importdata(vartable, functable)
        commandLexer = Lexer(scopedVariableTable)

        if cases.get(tc[1]):
            for i in cases[tc[1]]:
                res, error = commandLexer.analyse_command(i)
                if error:
                    return res, error
                if res is not None:
                    print(res)
        elif cases.get("default"):
            for i in cases["default"]:
                res, error = commandLexer.analyse_command(i)
                if error:
                    return res, error
                if res is not None:
                    print(res)

        return None, None

    def ternary_operator(self, tc: list) -> tuple[type(None), type(None)]:
        condition_end_pos = 1
        truecase = []
        falsecase = []
        # Positions = "condition" [0], "truecase" [1], "falsecase" [2]
        current_position = 0
        loopIndex = 0
        currentCommand = []
        for i in tc[1:]:
            loopIndex += 1
            if i == ":":
                if current_position == 0:
                    condition_end_pos = loopIndex
                    currentCommand = []
                elif current_position == 1:
                    truecase.append(currentCommand)
                    currentCommand = []
                elif current_position == 2:
                    falsecase.append(currentCommand)
                    currentCommand = []
                current_position += 1
                continue
            if i == "&&":
                if current_position == 0:
                    return (
                        'InvalidSyntax: "&&" cannot be used in Conditions.',
                        Exceptions.InvalidSyntax,
                    )
                if current_position == 1:
                    truecase.append(currentCommand)
                    currentCommand = []
                elif current_position == 2:
                    falsecase.append(currentCommand)
                    currentCommand = []
                continue
            currentCommand.append(i)
        runCode = self.parser.parse_conditions(
            self.parser.parse_condition_list(tc[1:condition_end_pos] + ["then"]),
            self.analyse_command,
        )
        if runCode:
            for i in truecase:
                res, error = self.analyse_command(i)
                if error:
                    return res, error
                if res is not None:
                    print(res)
        else:
            for i in falsecase:
                res, error = self.analyse_command(i)
                if error:
                    return res, error
                if res is not None:
                    print(res)
        return None, None

    def handle_base_keywords(self, tc: list) -> tuple[Any, Any]:
        all_variable_name: list = self.symbol_table.get_all_variable_name()
        all_function_name: list = self.symbol_table.get_all_function_name()

        if tc[0] in PRIMITIVE_TYPE:
            try:
                definedType = self.parser.parse_type_string(tc[0])
                if tc[1] in all_variable_name:
                    return (
                        f"AlreadyDefined: a Variable {tc[1]} is already defined",
                        Exceptions.AlreadyDefined,
                    )

                # Checking for variable naming violation
                if not self.parser.check_naming_violation(tc[1]):
                    return (
                        "InvalidValue: a Variable name cannot start with digits or keywords.",
                        Exceptions.InvalidValue,
                    )

                # var(0) a(1) =(2) 3(3)
                value = " ".join(tc[3:])
                is_dynamic = False
                if value.startswith("new Dynamic ("):
                    is_dynamic = True
                    value = value[13:-1]
                res, error = self.analyse_command(value.split())
                if error:
                    return res, error
                if definedType == Types.Float:
                    if isinstance(res, mathParser.values.Number):
                        res = float(res.value)
                    else:
                        res = float(res)

                vartype = self.parser.parse_type_from_value(res)
                if vartype == Types.Integer and definedType == Types.Float:
                    vartype = Types.Float
                # Checks If existing variable type matches the New value type
                if tc[0] != "var" and definedType != vartype and not is_dynamic:
                    return (
                        "InvalidValue: Variable types doesn't match value type.",
                        Exceptions.InvalidValue,
                    )
                if vartype == Exceptions.InvalidSyntax:
                    return "InvalidSyntax: Invalid value", Exceptions.InvalidSyntax
                res = self.parser.parse_escape_character(res)
                if res in all_variable_name:
                    res = self.symbol_table.GetVariable(res)[1]
                self.symbol_table.set_variable(tc[1], res, vartype)
                return None, None
            except IndexError:
                # var(0) a(1)
                if tc[0] == "var":
                    return (
                        "InvalidSyntax: Initial value needed for var keyword",
                        Exceptions.InvalidSyntax,
                    )
                vartype = self.parser.parse_type_string(tc[0])
                if vartype == Exceptions.InvalidSyntax:
                    return "InvalidSyntax: Invalid type", Exceptions.InvalidSyntax
                self.symbol_table.set_variable(tc[1], None, vartype)
                return None, None
        elif tc[0] in LISTDECLARE_KEYW:
            # Checking for variable naming violation
            if not self.parser.check_naming_violation(tc[1]):
                return (
                    "InvalidValue: a Variable name cannot start with digits or keywords.",
                    Exceptions.InvalidValue,
                )
            # int[] arr = new int [5][5]
            arrType = self.parser.parse_type_string(tc[0][:-2])
            # Check if the declaration was `new int[5][5]` or `new int [5][5]`
            if tc[4].endswith("]"):
                arrShape = tc[4][len(tc[0][:-2]) :][1:-1]
                if arrShape.find("][") != -1:
                    arrShape = arrShape.split("][")
                if len(arrShape) <= 0:
                    arrSize = []
                else:
                    arrSize = list(map(int, arrShape))
            else:
                arrShape = " ".join(tc[5:])[1:-1].split("][")
                if len(arrShape) == 0:
                    arrSize = []
                else:
                    arrSize = list(map(int, arrShape))
            print(
                "Array type:",
                arrType,
                "\nArray shape:",
                arrSize,
                "\nArray dimension:",
                len(arrSize),
            )
            self.symbol_table.set_variable(
                tc[1],
                Array(
                    arrType,
                    arrSize,
                    np.array(
                        [b"0"] * arrSize[len(arrSize) - 1],
                        ndmin=len(arrSize),
                        dtype=self.parser.type_string_to_numpy_type(tc[0][:-2]),
                    ),
                ),
                Types.Array
            )
            return None, None
        elif tc[0] == "if":
            return self.if_else_statement(tc)
        elif tc[0] == "throw":
            # Go to the Throw keyword function
            return self.throw_keyword(tc)
        elif tc[0] == "del":
            if tc[1] in all_variable_name:
                self.symbol_table.DeleteVariable(tc[1])
                return None, None
            if tc[1] in all_function_name:
                self.symbol_table.DeleteFunction(tc[1])
                return None, None
            return (
                "InvalidValue: The Input is not a variable.",
                Exceptions.InvalidValue,
            )
        elif tc[0] == "loopfor":
            return self.loopfor_statement(tc)
        elif tc[0] == "switch":
            return self.switch_case_statement(tc)
        elif tc[0] == "?":
            return self.ternary_operator(tc)
        elif tc[0] == "import":
            if tc[1] == "all":
                with open(f"{tc[2]}.sts") as f:
                    for i in f.readlines():
                        self.analyse_command(i)
        else:
            return (
                "NotImplementedException: This feature is not implemented",
                Exceptions.NotImplementedException,
            )

    def analyse_command(self, tc: list) -> tuple[Any, Any]:
        if len(tc) == 0:
            return None, None

        all_variable_name: list = self.symbol_table.get_all_variable_name()
        all_function_name: list = self.symbol_table.get_all_function_name()
        functioncall: list = " ".join(tc).split(".")

        def parse_argument(argumentstring, seperator):
            argument = ""
            in_paren = 0
            for i in seperator.join(argumentstring):
                if i == "(":
                    in_paren += 1
                    if in_paren == 1:
                        continue
                if in_paren > 0:
                    if i == ")":
                        in_paren -= 1
                        if in_paren == 0:
                            break
                    argument += i
            return argument

        if tc[0] in all_variable_name:
            try:
                return self.variable_setting(tc)
            except IndexError:
                var = self.symbol_table.GetVariable(tc[0])[1]
                if isinstance(var, str):
                    if var.startswith("new Dynamic ("):
                        var = var.removeprefix("new Dynamic (")
                        if var.endswith(")"):
                            var = var[:-1]
                return var, None
        elif " ".join(tc[0:]).split("(")[0].strip() == "typeof":
            value = parse_argument(tc[0:], " ")

            res, error = self.analyse_command(value.split())
            if error:
                return res, error

            res = self.parser.parse_type_from_value(res)
            if res == Exceptions.InvalidSyntax:
                return (
                    "InvalidSyntax: A String must starts with Quote and End with quote.",
                    Exceptions.InvalidSyntax,
                )
            return f'"{res.value}"', None
        elif " ".join(tc[0:]).split("(")[0].strip() == "print":
            value = parse_argument(tc[0:], " ")

            res, error = self.analyse_command(value.split())
            if error:
                return res, error
            res = str(res)
            if res.startswith("new Dynamic ("):
                res = res.removeprefix("new Dynamic (")
                if res.endswith(")"):
                    res = res[:-1]
            if res.startswith('"'):
                res = res[1:]
            if res.endswith('"'):
                res = res[:-1]
            value = self.parser.parse_escape_character(res)
            return value, None
        elif " ".join(tc[0:]).split("(")[0].strip() == "input":
            value = parse_argument(tc[0:], " ")

            if value.startswith("new Dynamic ("):
                value = value.removeprefix("new Dynamic (")[:-1]
            value, error = self.analyse_command(value.split())
            if error:
                return value, error

            if isinstance(value, str):
                if value.startswith('"'):
                    value = value[1:]
                if value.endswith('"'):
                    value = value[:-1]
            if value is None:
                value = ""
            res = input(str(value))  # Recieve the Input from the User
            return f'"{res}"', None  # Return the Recieved Input
        elif " ".join(tc[0:]).split("(")[0].strip() == "exit":
            value = parse_argument(tc[0:], " ")
            valtype = self.parser.parse_type_from_value(value)
            if value.startswith('"'):
                value = value[1:]
            if value.endswith('"'):
                value = value[:-1]
            return f"EXITREQUEST {value}", valtype
        elif tc[0] in BASE_KEYWORDS:
            return self.handle_base_keywords(tc)
        elif len(functioncall) > 1:
            if functioncall[0] in PRIMITIVE_TYPE:
                if functioncall[0] == "int":
                    # Parse the function name. (Space safe)
                    function_name = functioncall[1].split("(")[0]
                    if function_name == "FromString":
                        argument, error = self.analyse_command(parse_argument(functioncall[1:], ".").split())
                        if error:
                            return res, error
                        if isinstance(argument, str) and argument.startswith('"') \
                            and argument.endswith('"'):
                            argument = argument[1:-1]
                        return int(argument), None
                    # Check If a float is a full number.
                    if function_name == "IsFloatFullNumber":
                        argument, error = self.analyse_command(parse_argument(functioncall[1:], ".").split())
                        if error:
                            return argument, error
                        if executor.check_is_float(argument):
                            return "false", None
                        else:
                            return "true", None
            else:
                res, error = self.parser.parse_expression(tc[0:])
                return res, error
        elif tc[0] in all_function_name:
            customSymbolTable = self.symbol_table
            functionObject = self.symbol_table.get_function(tc[0])
            flex = Lexer(customSymbolTable, self.parser)
            res, error = flex.analyse_command(functionObject[1])
            return res, error
        elif tc[0] == "//":
            return None, None
        else:
            res, error = self.parser.parse_expression(tc[0:])
            return res, error
