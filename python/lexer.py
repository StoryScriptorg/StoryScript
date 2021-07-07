from langParser import Parser
from executor import Executor
from langEnums import Exceptions, Types
from string import ascii_letters


# This class is used to store variables and function
class SymbolTable:
    def __init__(self):
        self.variable_table = {
            "true": (Types.Boolean, "true"),
            "false": (Types.Boolean, "false"),
        }
        self.function_table = {}
        self.enable_function_feature = False

    def copyvalue(self):
        return self.variable_table, self.function_table, self.enable_function_feature

    def importdata(self, variableTable, functionTable, enableFunctionFeature):
        self.variable_table = variableTable
        self.function_table = functionTable
        self.enable_function_feature = enableFunctionFeature

    def get_all_variable_name(self):
        return self.variable_table.keys()

    def GetVariable(self, key):
        return self.variable_table[key]

    def GetVariableType(self, key):
        return self.variable_table[key][0]

    def get_all_function_name(self):
        return self.function_table.keys()

    def get_function(self, key):
        return self.function_table[key]

    def SetVariable(self, key, value, vartype):
        self.variable_table[key] = (vartype, value)

    def setFunction(self, key, value, arguments):
        self.function_table[key] = (arguments, value)

    def DeleteVariable(self, key):
        del self.variable_table[key]

    def DeleteFunction(self, key):
        del self.function_table[key]


class Lexer:
    def __init__(self, symbolTable, executor=None, parser=None):
        self.executor = executor
        self.symbol_table = symbolTable
        self.parser = parser

        if executor is None:
            self.executor = Executor(self.symbol_table)

        if parser is None:
            self.parser = Parser(self.executor)

    def throwKeyword(self, tc, multipleCommandsIndex):
        # Throw keyword. "throw [Exception] [Description]"
        def getDescription():
            msg = ""
            for i in tc[2 : multipleCommandsIndex + 1]:
                if i.startswith('"'):
                    i = i[1:]
                if i.endswith('"'):
                    i = i[:-1]
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
            if tc[2 : multipleCommandsIndex + 1]:
                description = getDescription()
        except IndexError:
            pass

        return f"{errstr}: {description}", errenum

    def variable_setting(self, tc, multipleCommandsIndex):
        # Error messages
        invalid_value = "InvalidValue: Invalid value"
        mismatch_type = "InvalidValue: Value doesn't match variable type."

        all_variable_name = self.symbol_table.get_all_variable_name()

        if tc[1] == "=":  # Set operator
            value = " ".join(tc[2 : multipleCommandsIndex + 1])
            is_dynamic = False
            if value.startswith("new Dynamic ("):
                is_dynamic = True
                value = value[13:-1]
            res, error = self.analyseCommand(value.split())
            if error:
                return res, error
            value = ""

            for i in tc[2 : multipleCommandsIndex + 1]:
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
            error = self.symbol_table.SetVariable(tc[0], res, vartype)
            if error:
                return error[0], error[1]
            return None, None
        if tc[1] == "+=":  # Add & Set operator
            vartype = self.symbol_table.GetVariableType(tc[0])
            keepFloat = False
            if vartype == Types.Float:
                keepFloat = True
            res, error = self.analyseCommand(tc[2 : multipleCommandsIndex + 1])
            if error:
                return res, error
            res, error = self.parser.parse_expression([tc[0], "+", str(res)], keepFloat)
            value = ""
            try:
                if tc[2] in all_variable_name:
                    tc[2] = (self.symbol_table.GetVariable(tc[2]))[1]
                if tc[4] in all_variable_name:
                    tc[4] = (self.symbol_table.GetVariable(tc[4]))[1]
            except IndexError:
                pass

            for i in tc[2 : multipleCommandsIndex + 1]:
                value += i + " "
            value = value[:-1]

            valtype = self.parser.parse_type_from_value(res)
            if valtype == Exceptions.InvalidSyntax:
                return invalid_value, Exceptions.InvalidValue

            # Check if Value Type matches Variable type
            if valtype != vartype:
                return mismatch_type, Exceptions.InvalidValue
            res = self.parser.parse_escape_character(res)
            error = self.symbol_table.SetVariable(tc[0], res, vartype)
            if error:
                return error[0], error[1]
            return None, None
        if tc[1] == "-=":  # Subtract & Set operator
            vartype = self.symbol_table.GetVariableType(tc[0])
            keepFloat = False
            if vartype == Types.Float:
                keepFloat = True
            res, error = self.parser.parse_expression(
                tc[2 : multipleCommandsIndex + 1], keepFloat
            )
            if error:
                return error[0], error[1]
            res, error = self.parser.parse_expression([tc[0], "-", str(res)], keepFloat)
            value = ""
            try:
                if tc[2] in all_variable_name:
                    tc[2] = (self.symbol_table.GetVariable(tc[2]))[1]
                if tc[4] in all_variable_name:
                    tc[4] = (self.symbol_table.GetVariable(tc[4]))[1]
            except IndexError:
                pass

            for i in tc[2 : multipleCommandsIndex + 1]:
                value += i + " "
            value = value[:-1]

            valtype = self.parser.parse_type_from_value(res)
            if valtype == Exceptions.InvalidSyntax:
                return invalid_value, Exceptions.InvalidValue

            # Check if Value Type matches Variable type
            if valtype != vartype:
                return mismatch_type, Exceptions.InvalidValue
            res = self.parser.parse_escape_character(res)
            error = self.symbol_table.SetVariable(tc[0], res, vartype)
            if error:
                return error[0], error[1]
            return None, None
        if tc[1] == "*=":  # Multiply & Set operator
            vartype = self.symbol_table.GetVariableType(tc[0])
            keepFloat = False
            if vartype == Types.Float:
                keepFloat = True
            res, error = self.parser.parse_expression(
                tc[2 : multipleCommandsIndex + 1], keepFloat
            )
            if error:
                return error[0], error[1]
            res, error = self.parser.parse_expression([tc[0], "*", str(res)], keepFloat)
            value = ""
            try:
                if tc[2] in all_variable_name:
                    tc[2] = (self.symbol_table.GetVariable(tc[2]))[1]
                if tc[4] in all_variable_name:
                    tc[4] = (self.symbol_table.GetVariable(tc[4]))[1]
            except IndexError:
                pass

            for i in tc[2 : multipleCommandsIndex + 1]:
                value += i + " "
            value = value[:-1]

            valtype = self.parser.parse_type_from_value(res)
            if valtype == Exceptions.InvalidSyntax:
                return invalid_value, Exceptions.InvalidValue

            # Check if Value Type matches Variable type
            if valtype != vartype:
                return mismatch_type, Exceptions.InvalidValue
            res = self.parser.parse_escape_character(res)
            error = self.symbol_table.SetVariable(tc[0], res, vartype)
            if error:
                return error[0], error[1]
            return None, None
        if tc[1] == "/=":  # Divide & Set operator
            vartype = self.symbol_table.GetVariableType(tc[0])
            keepFloat = False
            if vartype == Types.Float:
                keepFloat = True
            res, error = self.parser.parse_expression(
                tc[2 : multipleCommandsIndex + 1], keepFloat
            )
            if error:
                return error[0], error[1]
            res, error = self.parser.parse_expression([tc[0], "/", str(res)], keepFloat)
            if error:
                return error[0], error[1]
            value = ""
            try:
                if tc[2] in all_variable_name:
                    tc[2] = (self.symbol_table.GetVariable(tc[2]))[1]
                if tc[4] in all_variable_name:
                    tc[4] = (self.symbol_table.GetVariable(tc[4]))[1]
            except IndexError:
                pass

            for i in tc[2 : multipleCommandsIndex + 1]:
                value += i + " "
            value = value[:-1]

            valtype = self.parser.parse_type_from_value(res)
            if valtype == Exceptions.InvalidSyntax:
                return invalid_value, Exceptions.InvalidValue

            # Check if Value Type matches Variable type
            if valtype != vartype:
                return mismatch_type, Exceptions.InvalidValue
            res = self.parser.parse_escape_character(res)
            error = self.symbol_table.SetVariable(tc[0], res, vartype)
            if error:
                return error[0], error[1]
            return None, None
        if tc[1] == "%=":  # Modulo Operaion & Set operator
            vartype = self.symbol_table.GetVariableType(tc[0])
            keepFloat = False
            if vartype == Types.Float:
                keepFloat = True
            res, error = self.analyseCommand(tc[2 : multipleCommandsIndex + 1])
            if error:
                return res, error
            res, error = self.parser.parse_expression([tc[0], "%", str(res)], keepFloat)
            value = ""
            try:
                if tc[2] in all_variable_name:
                    tc[2] = (self.symbol_table.GetVariable(tc[2]))[1]
                if tc[4] in all_variable_name:
                    tc[4] = (self.symbol_table.GetVariable(tc[4]))[1]
            except IndexError:
                pass

            for i in tc[2 : multipleCommandsIndex + 1]:
                value += i + " "
            value = value[:-1]

            valtype = self.parser.parse_type_from_value(res)
            if valtype == Exceptions.InvalidSyntax:
                return invalid_value, Exceptions.InvalidValue

            # Check if Value Type matches Variable type
            if valtype != vartype:
                return mismatch_type, Exceptions.InvalidValue
            res = self.parser.parse_escape_character(res)
            error = self.symbol_table.SetVariable(tc[0], res, vartype)
            if error:
                return error[0], error[1]
            return None, None
        res, error = self.parser.parse_expression(tc[0 : multipleCommandsIndex + 1])
        if error:
            return error[0], error[1]
        return res, None

    def if_else_statement(self, tc):
        runCode = self.parser.parse_conditions(
            self.parser.parse_condition_list(tc[1:]), self.analyseCommand
        )

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
                res, error = self.analyseCommand(i)
                if error:
                    return res, error
                if res is not None:
                    print(res)
        else:
            # Iterate through commands
            for i in ifstatement["else"]:
                res, error = self.analyseCommand(i)
                if error:
                    return res, error
                if res is not None:
                    print(res)

        return None, None

    def loopfor_statement(self, tc):
        all_variable_name = self.symbol_table.get_all_variable_name()
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
            vartable, functable, isenablefunction = self.symbol_table.copyvalue()
            scopedVariableTable = SymbolTable()
            scopedVariableTable.importdata(vartable, functable, isenablefunction)
            commandlexer = Lexer(scopedVariableTable)
            index = 0
            if tc[1].endswith(":"):
                tc[1] = tc[1][:-1]
            if tc[1] in all_variable_name:
                tc[1] = self.symbol_table.GetVariable(tc[1])[1]
            times = int(tc[1])
            while index < times:
                scopedVariableTable = SymbolTable()
                scopedVariableTable.importdata(vartable, functable, isenablefunction)
                commandlexer.symbol_table = scopedVariableTable
                for i in commands:
                    res, error = commandlexer.analyseCommand(i)
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

    def switch_case_statement(self, tc):
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
        vartable, functable, isenablefunction = self.symbol_table.copyvalue()
        scopedVariableTable.importdata(vartable, functable, isenablefunction)
        commandLexer = Lexer(scopedVariableTable)

        try:
            for i in cases[tc[1]]:
                res, error = commandLexer.analyseCommand(i)
                if error:
                    return res, error
                if res is not None:
                    print(res)
        except KeyError:
            try:
                for i in cases["default"]:
                    res, error = commandLexer.analyseCommand(i)
                    if error:
                        return res, error
                    if res is not None:
                        print(res)
            except KeyError:
                pass

        return None, None

    def ternary_operator(self, tc):
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
            self.analyseCommand,
        )
        if runCode:
            for i in truecase:
                self.analyseCommand(i)
        else:
            for i in falsecase:
                self.analyseCommand(i)
        return None, None

    def analyseCommand(self, tc):
        multipleCommandsIndex = -1
        # All Keywords
        basekeywords = [
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
            "#define",
            "dynamic",
            "loopfor",
            "switch",
            "input",
            "exit",
            "?",
            "void",
        ]

        for i in tc:
            multipleCommandsIndex += 1
            if i == "&&":
                break

        all_variable_name = self.symbol_table.get_all_variable_name()
        allFunctionName = self.symbol_table.get_all_function_name()

        # Error messages
        paren_needed = "InvalidSyntax: Parenthesis is needed after a function name"
        close_paren_needed = (
            "InvalidSyntax: Parenthesis is needed after an Argument input"
        )

        if tc[0] in all_variable_name:
            try:
                return self.variable_setting(tc, multipleCommandsIndex)
            except IndexError:
                var = self.symbol_table.GetVariable(tc[0])[1]
                if var.startswith("new Dynamic ("):
                    var = var.removeprefix("new Dynamic (")
                    if var.endswith(")"):
                        var = var[:-1]
                return var, None
        elif tc[0] in basekeywords:
            if tc[0] in [
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
            ]:
                try:
                    definedType = self.parser.parse_type_string(tc[0])
                    if tc[1] in self.symbol_table.get_all_variable_name():
                        return (
                            f"AlreadyDefined: a Variable {tc[1]} is already defined",
                            Exceptions.AlreadyDefined,
                        )

                    # Checking for variable naming violation
                    if not self.parser.check_naming_violation(tc[1]):
                        return (
                            "InvalidValue: a Variable name cannot start with digits.",
                            Exceptions.InvalidValue,
                        )

                    # var(0) a(1) =(2) 3(3)
                    value = " ".join(tc[3 : multipleCommandsIndex + 1])
                    is_dynamic = False
                    if value.startswith("new Dynamic ("):
                        is_dynamic = True
                        value = value[13:-1]
                    res, error = self.analyseCommand(value.split())
                    if error:
                        return res, error
                    if definedType == Types.Float:
                        res = float(res)

                    vartype = self.parser.parse_type_from_value(res)
                    if vartype == Types.Integer and definedType == Types.Float:
                        vartype = Types.Float
                    if tc[0] != "var":
                        # Check If existing variable type matches the New value type
                        if definedType != vartype and not is_dynamic:
                            return (
                                "InvalidValue: Variable types doesn't match value type.",
                                Exceptions.InvalidValue,
                            )
                    if vartype == Exceptions.InvalidSyntax:
                        return "InvalidSyntax: Invalid value", Exceptions.InvalidSyntax
                    res = self.parser.parse_escape_character(res)
                    if res in all_variable_name:
                        res = self.symbol_table.GetVariable(res)[1]
                    error = self.symbol_table.SetVariable(tc[1], res, vartype)
                    if error:
                        return error[0], error[1]
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
                    self.symbol_table.SetVariable(tc[1], None, vartype)
                    return None, None
            elif tc[0] == "print":
                value = ""
                for i in tc[1 : multipleCommandsIndex + 1]:
                    value += i + " "
                value = value[:-1]
                if not value.startswith(
                    "("
                ):  # Check If the expression has parentheses around or not
                    return (
                        paren_needed,
                        Exceptions.InvalidSyntax,
                    )  # Return error if not exists
                if not value.endswith(
                    ")"
                ):  # Check If the expression has parentheses around or not
                    return (
                        close_paren_needed,
                        Exceptions.InvalidSyntax,
                    )  # Return error if not exists
                value = value[1:-1]
                svalue = value.split()
                res, error = self.analyseCommand(svalue)
                if error:
                    return res, error
                if value in all_variable_name:
                    value = self.symbol_table.GetVariable(value)[1]
                value = str(value)
                if value.startswith("new Dynamic ("):
                    value = value[13:]
                    if value.endswith(")"):
                        value = value[:-1]
                if value.startswith('"'):
                    value = value[1:]
                if value.endswith('"'):
                    value = value[:-1]
                if error:
                    return value, error
                value = self.parser.parse_escape_character(value)
                return value, None
            elif tc[0] == "input":
                value = ""
                for i in tc[
                    1 : multipleCommandsIndex + 1
                ]:  # Get all parameters provided as 1 long string
                    value += i + " "
                value = value[:-1]
                if not value.startswith(
                    "("
                ):  # Check If the expression has parentheses around or not
                    return (
                        paren_needed,
                        Exceptions.InvalidSyntax,
                    )  # Return error if not exists
                if not value.endswith(
                    ")"
                ):  # Check If the expression has parentheses around or not
                    return (
                        close_paren_needed,
                        Exceptions.InvalidSyntax,
                    )  # Return error if not exists
                value = value[1:-1]  # Cut parentheses out of the string
                if value.startswith('"'):
                    value = value[1:]
                if value.endswith('"'):
                    value = value[:-1]
                res = input(value)  # Recieve the Input from the User
                return f'"{res}"', None  # Return the Recieved Input
            elif tc[0] == "if":
                return self.if_else_statement(tc)
            elif tc[0] == "exit":
                value = ""
                for i in tc[
                    1 : multipleCommandsIndex + 1
                ]:  # Get all parameters provided as 1 long string
                    value += i + " "
                value = value[:-1]
                if not value.startswith(
                    "("
                ):  # Check If the expression has parentheses around or not
                    return (
                        paren_needed,
                        Exceptions.InvalidSyntax,
                    )  # Return error if not exists
                if not value.endswith(
                    ")"
                ):  # Check If the expression has parentheses around or not
                    return (
                        close_paren_needed,
                        Exceptions.InvalidSyntax,
                    )  # Return error if not exists
                value = value[1:-1]
                valtype = self.parser.parse_type_from_value(value)
                if value.startswith('"'):
                    value = value[1:]
                if value.endswith('"'):
                    value = value[:-1]
                return f"EXITREQUEST {value}", valtype
            elif tc[0] == "#define":
                try:
                    # Set Interpreter Settings
                    if tc[1] == "interpet" and tc[2] == "enableFunction":
                        if tc[3] == "true":
                            self.symbol_table.enable_function_feature = True
                            return None, None
                        self.symbol_table.enable_function_feature = False
                        return None, None
                except IndexError:
                    return (
                        "InvalidValue: You needed to describe what you will change.",
                        Exceptions.InvalidValue,
                    )
            elif tc[0] == "throw":
                return self.throwKeyword(
                    tc, multipleCommandsIndex
                )  # Go to the Throw keyword function
            elif tc[0] == "typeof":
                if tc[1].startswith("("):
                    tc[1] = tc[1][1:]
                else:
                    return paren_needed, Exceptions.InvalidSyntax
                if tc[multipleCommandsIndex].endswith(")"):
                    tc[multipleCommandsIndex] = tc[multipleCommandsIndex][:-1]
                else:
                    return close_paren_needed, Exceptions.InvalidSyntax
                if tc[1] in all_variable_name:
                    return self.symbol_table.GetVariableType(tc[1]), None
                res, error = self.parser.parse_expression(
                    tc[1 : multipleCommandsIndex + 1]
                )
                if error:
                    return error[0], error[1]

                if not tc[1] in all_variable_name and tc[1][0] in ascii_letters:
                    return (
                        f"InvalidValue: {tc[1]} is not a Variable and Is not a String.",
                        Exceptions.InvalidValue,
                    )
                res = self.parser.parse_type_from_value(res)
                if res == Exceptions.InvalidSyntax:
                    return (
                        'InvalidSyntax: A String must starts with Quote (") and End with quote (")',
                        Exceptions.InvalidSyntax,
                    )
                return res, None
            elif tc[0] == "del":
                if tc[1] in all_variable_name:
                    self.symbol_table.DeleteVariable(tc[1])
                    return None, None
                if tc[1] in allFunctionName:
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
                            self.analyseCommand(i)
            else:
                return (
                    "NotImplementedException: This feature is not implemented",
                    Exceptions.NotImplementedException,
                )
        elif tc[0] in allFunctionName:
            customSymbolTable = self.symbol_table
            functionObject = self.symbol_table.get_function(tc[0])
            flex = Lexer(customSymbolTable, self.executor, self.parser)
            res, error = flex.analyseCommand(functionObject[1])
            return res, error
        elif tc[0] == "//":
            return None, None
        else:
            res, error = self.parser.parse_expression(tc[0 : multipleCommandsIndex + 1])
            if isinstance(res, bool):
                res = self.parser.parse_conditions(
                    self.parser.parse_condition_list(tc[1:]), self.analyseCommand
                )
            return res, error
