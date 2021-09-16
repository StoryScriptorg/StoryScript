import numpy as np
from langData import *
from typing import NoReturn
from langParser import Parser
# from cachelogger import CacheLogger
from SymbolTable import SymbolTable
import mathParser.values
import executor


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

    def variable_setting(self, tc: list, original_text) -> tuple:
        all_variable_name = self.symbol_table.get_all_variable_name()

        if tc[1] == "=":  # Set operator
            value = " ".join(tc[2:])
            if value.startswith("new Dynamic"):
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
            vartype = self.symbol_table.get_variable_type(tc[0])
            # Check if Value Type matches Variable type
            if valtype != vartype:
                return f"{mismatch_type} Expected {vartype.value}, Found {valtype.value}.", Exceptions.InvalidValue
            if vartype == Types.Action:
                self.symbol_table.set_function(tc[0], res)
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
            res, error = self.parser.parse_expression(original_text)
            return res, error

        vartype = self.symbol_table.get_variable_type(tc[0])
        keepFloat = False
        if vartype == Types.Float:
            keepFloat = True
        res, error = self.analyse_command(tc[2:])
        if error:
            return res, error
        res, error = self.parser.parse_expression(
            f"{tc[0]} {operator} {str(res)}", keepFloat
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
        if vartype == Types.Action:
            if operator == "+":
                return "InvalidOperatorException: You cannot use += with lambda expression, maybe you are looking for Event?", Exceptions.InvalidOperatorException
            return f"InvalidOperatorException: You cannot use {operator}= with lambda expression.", Exceptions.InvalidOperatorException
        self.symbol_table.set_variable(tc[0], res, vartype)
        return None, None

    def if_else_statement(self, tc: list) -> tuple:
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
                    if isinstance(res, str) and res.startswith("EXITREQUEST"):
                        return res, error
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

    def loopfor_statement(self, tc: list) -> tuple:
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
            times, error = self.analyse_command([tc[1]])
            if error:
                return times, error
            times = int(times)
            while index < times:
                scoped_variable_table = SymbolTable()
                scoped_variable_table.importdata(vartable, functable)
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

    def switch_case_statement(self, tc: list) -> tuple:
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

    def ternary_operator(self, tc: list) -> tuple:
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
    
    def parse_lambda_expression(self, tc):
        # Lambda expression
        # Syntax: lambda return (arguments) => function body && another expression
        # Example: lambda void () => print("Hello!")
        return_type = self.parser.parse_type_string(tc[1])
        joined_expr = " ".join(tc[2:])
        in_arguments_list = False
        in_function_body = False
        is_found_equal_sign = False
        function_body = ""
        arguments = ""
        
        for i in joined_expr:
            if in_function_body:
                function_body += i
            elif i == "=":
                is_found_equal_sign = True
            elif i == ">" and is_found_equal_sign:
                is_found_equal_sign = False
                in_function_body = True
            elif i == "(":
                in_arguments_list = True
            elif i == ")":
                in_arguments_list = False
            elif in_arguments_list:
                if is_found_equal_sign:
                    arguments += "="
                arguments += i
                is_found_equal_sign = False

        existing_arguments: set = set()
        def parse_function_argument(arg):
            arg = arg.split()
            arg[0] = self.parser.parse_type_string(arg[0])
            if arg[1] in existing_arguments:
                # Raise an error if an argument is defined multiple times
                raise ValueError(f"Arguments named \"{arg[1]}\" is defined multiple times (in lambda expression). Please consider renaming the argument.")
            if arg[1] in all_variable_name or arg[1] in all_function_name:
                raise ValueError(f"an Argument named \"{arg[1]}\" is already defined either as a function or a variable. Please consider renaming the argument.")
            existing_arguments.add(arg[1])
            return arg
        try:
            args = arguments.split(",")
            if not args[0]:
                args = []
            else:
                arguments = list(map(parse_function_argument, args))
        except ValueError as e:
            # Handle the error if an argument is defined multiple times
            return f"AlreadyDefined: {e}", Exceptions.AlreadyDefined
        return LambdaExpr(arguments, return_type, function_body), None
    
    def imports_map_methods(self, module):
        print("[DEBUG] Importing a python file and manually mapping...")
        def function_type():
            pass
        for i in dir(module):
            # Skip private functions
            if i.startswith("_"):
                continue
            attr = getattr(module, i)
            if isinstance(attr, type):
                print("[INFO] Class found. Skipping...")
                continue
            # Check If the method is not a function
            if not isinstance(attr, (type(function_type), type(self.imports_map_methods))):
                continue
            # Assemble the Python function object from the available information.
            self.symbol_table.set_function(i, PythonFunctionObject(attr.__annotations__.get("return"), attr.__name__, attr.__code__.co_varnames, attr))
    
    def handle_imports(self, tc: list) -> tuple:
        if len(tc) < 2:
            return not_enough_args_for_import_statement, Exceptions.NotDefinedException
        if tc[1] == "all":
            if len(tc) < 3:
                return not_enough_args_for_import_statement, Exceptions.NotDefinedException
            filepath, error = self.analyse_command(f"print({' '.join(tc[2:])})".split(), original_text=f"print({' '.join(tc[2:])})")
            if error:
                return filepath, error
            # Dependencies importing
            # if filepath in MODULES:
            #     modules_info = __import__(MODULES[filepath])
            with open(filepath) as f:
                for i in f.readlines():
                    self.analyse_command(i)
            return None, None
        filepath, error = self.analyse_command(f"print({' '.join(tc[1:])})".split())
        if error:
            return filepath, error
        if filepath.startswith("python:"):
            # If the user meant to import python files
            filepath = filepath.removeprefix("python:")
            if filepath.endswith(".py"):
                filepath = filepath[:-3]
            module = __import__(filepath)
            if hasattr(module, "STORYSCRIPT_METHOD_MAPPING") and module.STORYSCRIPT_METHOD_MAPPING:
                if not hasattr(module, "METHODS"):
                    return f"NotDefinedException: File {filepath} is trying to map methods, but no method mapping dictionary is found.", Exceptions.NotDefinedException
                for i in module.METHODS:
                    method = module.METHODS[i]
                    if isinstance(method, dict):
                        try:
                            method = PythonFunctionObject(method["return_type"], method["name"], method["arguments"], method["action"])
                            self.symbol_table.set_function(i, method)
                            continue
                        except KeyError:
                            return (
                                f"InvalidValue: The method \"{i}\" dictionary is missing a key.",
                                Exceptions.InvalidValue,
                            )
                    return f"InvalidTypeException: Unknown method mapping type. (Error occurred while scanning method \"{i}\")", Exceptions.InvalidTypeException
            else:
                self.imports_map_methods(module)
        return None, None
    
    def handle_new_keyword(self, tc: list, original_text: str) -> tuple:
        class_name = original_text.split("(")[0].strip().removeprefix("new").strip()
        if class_name == "Dynamic":
            return original_text, None
        # new type[shape]
        def finalizeShape(shape):
            res, error = self.analyse_command(shape.split())
            if error:
                raise ValueError(res)
            return int(res)

        # Check if the declaration was `new int[5][5]` or `new int [5][5]`
        arrtype = None
        arrSize = []
        if tc[1].endswith("]"):
            arrtype = tc[1].split("[")[0]
            arrShape = tc[1][len(arrtype):][1:-1]
            if arrShape.find("][") != -1:
                arrShape = arrShape.split("][")
            else:
                arrShape = [arrShape]
            if len(arrShape) <= 0:
                arrSize = []
            else:
                try:
                    arrSize = list(map(finalizeShape, arrShape))
                except ValueError as ve:
                    return str(ve), getattr(Exceptions, str(ve).split(":")[0])
        else:
            # new int [5][5]
            arrtype = tc[1]
            arrShape = " ".join(tc[2:])[1:-1]
            if arrShape.find("][") != -1:
                arrShape = arrShape.split("][")
            else:
                arrShape = [arrShape]
            if not arrShape:
                return "NotDefinedException: Array shape cannot be empty!", Exceptions.NotDefinedException
            arrSize = list(map(finalizeShape, arrShape))
        
        init_val = b"0"
        args = {"ndmin": len(arrSize)}
        if arrtype == "int":
            init_val = 0
            args["dtype"] = "i"
        elif arrtype == "float":
            init_val = 0
            args["dtype"] = "f"
        elif arrtype == "string":
            init_val = ""
            args["dtype"] = "S"
        elif arrtype == "bool":
            init_val = False

        return Array(
                arrtype, arrSize,
                np.array(
                    [init_val] * arrSize[-1],
                    **args
                ),
            ), None
    
    def handle_variable_declaration(self, tc: list) -> tuple:
        all_variable_name = self.symbol_table.get_all_variable_name()

        if tc[0] == "void":
            return "InvalidTypeException: void is not eligible as a type for variable.", Exceptions.InvalidTypeException
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
            if value.startswith("new Dynamic"):
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
            if tc[0] != "var" and definedType != vartype and not is_dynamic and res not in {"null", None}:
                return (
                    f"{mismatch_type} Expected {definedType.value}, found {vartype.value}.",
                    Exceptions.InvalidValue,
                )
            if vartype == Exceptions.InvalidSyntax:
                return "InvalidSyntax: Invalid value", Exceptions.InvalidSyntax
            if vartype == Types.Action:
                self.symbol_table.set_function(tc[1], res)
            if res is None:
                res = "null"
            self.symbol_table.set_variable(tc[1], res, definedType)
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
            self.symbol_table.set_variable(tc[1], "null", vartype)
            return None, None
    
    def handle_array_declaration(self, tc: list, all_variable_name: list) -> tuple:
        # Checking for variable naming violation
        if not self.parser.check_naming_violation(tc[1]):
            return (
                "InvalidValue: a Variable name cannot start with digits or keywords.",
                Exceptions.InvalidValue,
            )
        if tc[1] in all_variable_name:
            return (
                f"AlreadyDefined: a Variable {tc[1]} is already defined",
                Exceptions.AlreadyDefined,
            )

        # int[] arr = new int [5][5]
        res, error = self.analyse_command(tc[3:])
        if error:
            return res, error
        self.symbol_table.set_variable(tc[1], res, Types.Array)
        return None, None

    def handle_base_keywords(self, tc: list, original_text: str) -> tuple:
        all_variable_name: list = self.symbol_table.get_all_variable_name()
        all_function_name: list = self.symbol_table.get_all_function_name()

        if tc[0] in PRIMITIVE_TYPE:
            return self.handle_variable_declaration(tc)
        if tc[0] in LISTDECLARE_KEYW:
            return self.handle_array_declaration(tc, all_variable_name)
        if tc[0] == "if":
            return self.if_else_statement(tc)
        if tc[0] == "throw":
            # Go to the Throw keyword function
            return self.parser.throw_keyword(tc, self.analyse_command)
        if tc[0] == "del":
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
        if tc[0] == "loopfor":
            return self.loopfor_statement(tc)
        if tc[0] == "switch":
            return self.switch_case_statement(tc)
        if tc[0] == "?":
            return self.ternary_operator(tc)
        if tc[0] == "import":
            return self.handle_imports(tc)
        if tc[0] == "lambda":
            return self.parse_lambda_expression(tc)
        if tc[0] == "new":
            return self.handle_new_keyword(tc, original_text)
        if tc[0] == "null":
            return "null", None

        return (
            "NotImplementedException: This feature is not implemented",
            Exceptions.NotImplementedException,
        )
    
    def handle_array_setting_variable_methods(self, functioncall: list, function_name: str) -> tuple:
        # Get the arguments list by splitting and trim the string
        arguments = list(map(lambda msg: msg.strip(), self.parser.split_arguments(self.parser.parse_argument(functioncall[1:], "."))))
        index = []
        value = None
        try:
            for i in arguments:
                if i.startswith("value") and i.find("=") != -1:
                    if value:
                        return "AlreadyDefined: value arguments is already defined. you cannot define it again.", Exceptions.AlreadyDefined
                    value, error = self.analyse_command(i.split("=")[1:], original_text=" ".join(i.split("=")[1:]))
                    if error:
                        return value, error
                else:
                    index_num, error = self.analyse_command([i], original_text=i)
                    if error:
                        return index_num, error
                    index.append(int(index_num))
        except ValueError as ve:
            return f"InvalidTypeException: {ve}", Exceptions.InvalidTypeException
        if not value:
            return "NotDefinedException: value arguments is required but not defined.", Exceptions.NotDefinedException
        old_data = self.symbol_table.GetVariable(functioncall[0])[1]
        new_data = old_data.data
        arrdups = []
        try:
            if len(index) > 1:
                # Multi-dimensional array accessing
                for i in index:
                    if arrdups == []:
                        arrdups.append(new_data[i])
                    else:
                        content = arrdups[-1][i]
                        if not isinstance(content, np.ndarray):
                            break
                        arrdups.append(content)
                if function_name == "AddOnIndex":
                    arrdups[-1][index[-1]] += value
                else:
                    arrdups[-1][index[-1]] = value
                # merge all array duplications into one array duplication
                for v, i in zip(enumerate(arrdups), index):
                    if v[0] + 1 >= len(arrdups) - 1:
                        break
                    v[1][i] = arrdups[v[0] + 1]
                    arrdups[v[0]] = v[1]
            else:
                if function_name == "AddOnIndex":
                    new_data[index] += value
                else:
                    new_data[index] = value
                arrdups.append(new_data)
        except IndexError as ie:
            return f"InvalidIndexException: {ie}", Exceptions.InvalidIndexException
        self.symbol_table.set_variable(functioncall[0], Array(old_data.dtype, old_data.shape, arrdups[0]), Types.Array)
        return None, None
    
    def handle_array_variable_methods(self, functioncall: list, function_name: str) -> tuple:
        if function_name == "Get":
            argument, error = self.analyse_command([self.parser.parse_argument(functioncall[1:], ".")])
            if error:
                return argument, error
            if not isinstance(argument, (mathParser.values.Number, int)):
                return f"InvalidTypeException: Expected argument #1 to be Number, Found {type(argument).__name__}", Exceptions.InvalidTypeException
            try:
                data = self.symbol_table.GetVariable(functioncall[0])[1].data[int(argument)]
                if isinstance(data, np.intc):
                    data = int(data)
                elif isinstance(data, np.str_):
                    data = str(data)
                elif isinstance(data, np.float64):
                    data = float(data)
                return data, None
            except IndexError as ie:
                return f"InvalidIndexException: {ie}", Exceptions.InvalidIndexException
        if function_name in {"Set", "AddOnIndex"}:
            return self.handle_array_setting_variable_methods(functioncall, function_name)
        if function_name == "Length":
            return len(self.symbol_table.GetVariable(functioncall[0])[1].data), None
    
    def handle_variable_methods(self, functioncall: list, function_name: str) -> tuple:
        vartype = self.symbol_table.get_variable_type(functioncall[0])
        if vartype == Types.Array:
            return self.handle_array_variable_methods(functioncall, function_name)
        if vartype == Types.Integer and function_name == "ToString":
            value = self.symbol_table.GetVariable(functioncall[0].strip())[1]
            if value == "null":
                return "InvalidTypeException: Cannot convert \"null\" (with type \"void\") to string!", Exceptions.InvalidTypeException
            return f"\"{value}\"", None

    def primitive_type_functions(self, functioncall: list, function_name: str) -> tuple:
        argument, error = self.analyse_command(self.parser.parse_argument(functioncall[1:], ".").split())
        if error:
            return argument, error
        if functioncall[0] == "int":
            if function_name == "FromString":
                if isinstance(argument, mathParser.values.Number):
                    return "InvalidTypeException: Expected argument #1 to be String, Found number.", Exceptions.InvalidTypeException
                if isinstance(argument, str) and argument.startswith('"') \
                    and argument.endswith('"'):
                    argument = argument[1:-1]
                try:
                    return int(argument), None
                except ValueError as e:
                    return f"InvalidValue: {e}", Exceptions.InvalidValue
            if function_name == "FromFloat":
                result = argument
                if not isinstance(argument, (mathParser.values.Number, int, float)):
                    return f"InvalidTypeException: Expected argument #1 to be Number, Found {type(argument).__name__}", Exceptions.InvalidTypeException
                if isinstance(argument, mathParser.values.Number):
                    result = int(argument.value)
                else:
                    result = int(argument)
                return result, None
            # Check If a float is a full number.
            if function_name == "IsFloatFullNumber":
                if executor.check_is_float(argument):
                    return "false", None
                return "true", None
        if functioncall[0] == "string" and function_name in {"FromInt", "FromFloat"}:
            if not isinstance(argument, mathParser.values.Number):
                try:
                    int(argument)
                except ValueError:
                    return f"InvalidTypeException: Expected argument #1 to be Number, Found {type(argument).__name__}", Exceptions.InvalidTypeException
            return f"\"{argument}\"", None
    
    def handle_function(self, functioncall: list, original_text: str) -> tuple:
        all_variable_name: list = self.symbol_table.get_all_variable_name()
        # Parse the function name. (Space safe)
        function_name = functioncall[1].split("(")[0]
        if functioncall[0].strip() in PRIMITIVE_TYPE:
            return self.primitive_type_functions(functioncall, function_name)
        if functioncall[0].strip() in all_variable_name:
            return self.handle_variable_methods(functioncall, function_name)
        res, error = self.parser.parse_expression(original_text)
        return res, error

    def analyse_command(self, tc: list, original_text: str = None) -> tuple:
        if len(tc) == 0 or tc[0] == "//":
            return None, None
        if not original_text:
            original_text = " ".join(tc[0:])

        all_variable_name: list = self.symbol_table.get_all_variable_name()
        all_function_name: list = self.symbol_table.get_all_function_name()
        functioncall: list = original_text.split(".")
        function_name = original_text.split("(")[0].strip()

        if tc[0] in all_variable_name:
            try:
                return self.variable_setting(tc, original_text)
            except IndexError:
                var = self.symbol_table.GetVariable(tc[0])[1]
                if isinstance(var, str) and var.startswith("new Dynamic ("):
                    var = var.removeprefix("new Dynamic (")
                    if var.endswith(")"):
                        var = var[:-1]
                return var, None
        elif function_name == "typeof":
            value = self.parser.parse_argument(original_text)

            res, error = self.analyse_command(value.split(), original_text=value)
            if error:
                return res, error

            res = self.parser.parse_type_from_value(res)
            return f'"{res.value}"', None
        elif function_name == "print":
            value = self.parser.parse_argument(original_text)
            res, error = self.analyse_command(value.split())
            if error:
                return res, error
            res = str(res)
            if res.startswith("new Dynamic ("):
                res = res.removeprefix("new Dynamic (")
                if res.endswith(")"):
                    res = res[:-1]
            if res.startswith('"') and res.endswith('"'):
                res = res[1:-1]
            return res, None
        elif function_name == "input":
            value = self.parser.parse_argument(original_text)

            if value.startswith("new Dynamic ("):
                value = value.removeprefix("new Dynamic (")[:-1]
            value, error = self.analyse_command(value.split(), original_text=value)
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
        elif function_name == "exit":
            value, error = self.analyse_command(self.parser.parse_argument(original_text))
            if error:
                return value, error
            if isinstance(value, str):
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
            if value is None:
                value = 0
            return f"EXITREQUEST {value}", None
        elif tc[0] in BASE_KEYWORDS:
            return self.handle_base_keywords(tc, original_text)
        elif function_name in all_function_name:
            custom_symbol_table = self.symbol_table
            function_object = self.symbol_table.get_function(function_name)

            # Parse arguments
            arguments = self.parser.split_arguments(self.parser.parse_argument(original_text))
            argpos = 0
            if isinstance(function_object, LambdaExpr):
                for value, name in zip(arguments, function_object.arguments):
                    res, error = self.analyse_command(value, original_text=value)
                    if error:
                        return res, error
                    valtype = self.parser.parse_type_from_value(res)
                    if isinstance(name[0], str):
                        name[0] = self.parser.parse_type_string(name[0])
                    if valtype != name[0]:
                        return f"InvalidTypeException: Invalid type, Expected {name[0].value} for argument #{argpos}, found {valtype.value}.", Exceptions.InvalidTypeException
                    custom_symbol_table.set_variable(name[1], res, name[0])
                    argpos += 1
            else:
                args = []
                for value in arguments:
                    res, error = self.analyse_command(value, original_text=value)
                    if error:
                        return res, error
                    if isinstance(res, mathParser.values.Number):
                        res = res.value
                    valtype = self.parser.parse_type_from_value(res)
                    args.append(res)
                try:
                    res = function_object.function_body(*args)
                    return res, None
                except Exception as e:
                    return f"(Python Exception): {e}", "(Python Exception)"

            flex = Lexer(custom_symbol_table, self.parser)
            res, error = flex.analyse_command(function_object.function_body.split(), original_text=function_object.function_body)
            for name in function_object.arguments:
                custom_symbol_table.DeleteVariable(name[1])
            if error:
                return res, error
            valtype = self.parser.parse_type_from_value(res)
            if valtype != function_object.return_type:
                return f"InvalidTypeException: Return value mismatched. Expected {function_object.return_type.value}, found {valtype.value}.", Exceptions.InvalidTypeException
            return res, error
        elif len(functioncall) > 1:
            return self.handle_function(functioncall, original_text)
        else:
            res, error = self.parser.parse_expression(original_text)
            return res, error
