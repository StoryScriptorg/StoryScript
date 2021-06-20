from string import ascii_letters, digits
from langEnums import Types, Exceptions, ConditionType

class Parser:
    def __init__(self, executor):
        self.executor = executor

    @staticmethod
    def parse_escape_character(trimmed_string):
        is_escape_char_detected = False
        outstr = ""
        for i in str(trimmed_string):
            outchar = i
            if i == "\\":
                is_escape_char_detected = True
                continue
            if is_escape_char_detected:
                is_escape_char_detected = False
                if i == "n":
                    outchar = "\n"
                elif i == "\\":
                    outchar = "\\"
                elif i == "t":
                    outchar = "\t"
                elif i == '"':
                    outchar = '"'
            outstr += outchar
        return outstr

    @staticmethod
    def parse_string_list(command):
        res = ""
        for i in command:
            res += i + " "
        res = res[:-1]
        return res

    @staticmethod
    def convert_to_python_native_type(valtype, value):
        """
        Returns a Python version of the value provided to a Type specified.
        [PARAMETER] valtype: Target output type
        [PARAMETER] value: The input value that will be converted.
        [RETURNS]
        a Converted value,
        Else the input value If the type is not support yet by the Converter.
        """
        if valtype == Types.Integer:
            return int(value)
        if valtype == Types.Float:
            return float(value)
        if value == Types.String:
            return str(value[1:-1])
        if value == Types.Boolean:
            if value == "true":
                return True
            if value == "false":
                return False
        return value

    @staticmethod
    def convert_to_storyscript_native_type(valtype, value):
        """
        Returns a Converted to StoryScript version of the value provided to a Type specified.
        [PARAMETER] valtype: Target output type
        [PARAMETER] value: The input value that will be converted.
        [RETURNS] a Converted value. Else the input value If the type is not support yet by the Converter.
        """
        if valtype == Types.Integer:
            return str(value)
        if valtype == Types.Float:
            return str(value)
        if value == Types.String:
            return f"\"{value}\""
        if value == Types.Boolean:
            if value:
                return "true"
            return "false"
        if value == Types.Dynamic:
            return f"new Dynamic ({value})"
        # If the types is not supported
        return value

    def parse_type_from_value(self, value):
        if not isinstance(value, str):
            value = str(value)
        is_float = self.executor.check_is_float(value)
        if value.startswith('"') or value.endswith('"'):
            if not (value.startswith('"') and value.endswith('"')):
                return Exceptions.InvalidSyntax
            return Types.String
        if value in ("true", "false"):
            return Types.Boolean
        if value.startswith("new List"):
            return Types.List
        if value.startswith("new Dictionary"):
            return Types.Dictionary
        if value.startswith("new Tuple"):
            return Types.Tuple
        if value.startswith("new Dynamic"):
            return Types.Dynamic
        if is_float:
            return Types.Float
        if not is_float:
            return Types.Integer
        return Exceptions.InvalidSyntax

    @staticmethod
    def parse_type_string(string):
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
        return Exceptions.InvalidSyntax

    @staticmethod
    def check_naming_violation(name):
        """ Returns If the variable naming valid or not """
        if not isinstance(name, str):
            name = str(name)
        if name in ["if", "else", "var", "int",
                        "bool", "float", "list", "dictionary",
                        "tuple", "const", "override", "func",
                        "end", "print", "input", "throw",
                        "string", "typeof", "del", "namespace", "?"]:
            return False
        if name[0] in digits:
            return False
        return True

    def parse_conditions(self, conditionslist, analyse_command_method):
        allexpr_result = []
        for i in conditionslist:
            expr_result = []
            current_condition_type = ConditionType.Single
            for j in i:
                if j and isinstance(j, list):
                    expr_result.append(self.parse_condition_expression(j, analyse_command_method))
                elif isinstance(j, ConditionType):
                    current_condition_type = j
            if current_condition_type == ConditionType.And:
                allexpr_result.append(all(expr_result))
            elif current_condition_type == ConditionType.Single:
                allexpr_result.append(expr_result[0])
            elif current_condition_type == ConditionType.Or:
                allexpr_result.append(any(expr_result))

        return all(allexpr_result)

    def parse_condition_expression(self, expr, analyse_command_method):
        """ Parse If the condition is True or False """
        # [:operator_index] = Accessing a Message before the operator
        # [operator_index + 1:] = Accessing a Message after the operator
        operator_index = 0
        for i in expr:
            if i in [">", "<", "==", "!=", ">=", "<="]:
                break
            operator_index += 1
        resl, error = analyse_command_method(expr[:operator_index]) # Analyse the message on the left
        if error:
            return resl, error

        resr, error = analyse_command_method(expr[operator_index + 1:]) # Analyse the message on the right
        if error:
            return resr, error

        # Type conversion
        restype = self.parse_type_from_value(resl)
        resl = self.convert_to_python_native_type(restype, resl)
        restype = self.parse_type_from_value(resr)
        resr = self.convert_to_python_native_type(restype, resr)

        if expr[operator_index] == "==": # If the operator was ==
            if resl == resr:
                return True
        elif expr[operator_index] == ">": # If the operator was >
            if resl > resr:
                return True
        elif expr[operator_index] == "<": # If the operator was <
            if resl < resr:
                return True
        elif expr[operator_index] == "!=": # If the operator was !=
            if resl != resr:
                return True
        elif expr[operator_index] == ">=": # If the operator was >=
            if resl >= resr:
                return True
        elif expr[operator_index] == "<=": # If the operator was <=
            if resl <= resr:
                return True
        else:
            return Exceptions.InvalidSyntax

        return False

    @staticmethod
    def parse_condition_list(expr):
        """ Separate expressions into a list of conditions """
        conditionslist:list = [] # List of conditions
        conditions:list = [] # List of condition
        condition:list = [] # Condition
        current_condition_type = ConditionType.Single # Current condition type
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

    def parse_expression(self, command, keep_float=False):
        try:
            expr = ""
            all_var_name = self.executor.symbol_table.get_all_variable_name()
            is_in_string = False
            for i in command:
                for j in i:
                    if j == '"':
                        if is_in_string:
                            is_in_string = False
                        else:
                            is_in_string = True
                if not is_in_string:
                    if i in all_var_name:
                        expr += self.executor.symbol_table.GetVariable(i)[1] + " "
                        continue
                expr += i + " "
            res = eval(expr)
            if isinstance(res, str):
                res = f"\"{res}\""
            if keep_float:
                return float(res), None
            try:
                if not self.executor.check_is_float(res):
                    return int(res), None
            except ValueError:
                pass
            return res, None
        except NameError as e:
            print("[PYTHON EVALUATION ERROR]")
            return f"NotDefinedException: {e}", Exceptions.NotDefinedException
        except SyntaxError as e:
            print("[PYTHON EVALUATION ERROR]")
            return f"InvalidSyntax: {e}", Exceptions.InvalidSyntax
        except TypeError as e:
            print("[PYTHON EVALUATION ERROR]")
            return f"InvalidTypeException: {e}", Exceptions.InvalidTypeException
