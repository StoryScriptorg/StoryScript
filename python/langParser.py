from string import ascii_letters, digits
from langEnums import Types, Exceptions, ConditionType

class Parser:
	def __init__(self, executor):
		self.executor = executor

	def parse_escape_character(self, trimmed_string):
		is_escape_char_detected = False
		outstr = ""
		for i in str(trimmedString):
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
			outstr += outchar
		return outstr

	def parse_string_list(self, command):
		res = ""
		for i in command:
			res += i + " "
		res = res[:-1]
		return res

	def convert_to_python_native_type(self, valtype, value):
		"""
		Returns a Converted to Python version of the value provided to a Type specified.
		[PARAMETER] valtype: Target output type
		[PARAMETER] value: The input value that will be converted.
		[RETURNS] a Converted value. Else the input value If the type is not support yet by the Converter.
		"""
		if valtype == Types.Integer:
			return int(value)
		elif valtype == Types.Float:
			return float(value)
		elif value == Types.String:
			return str(value[1:-1])
		elif value == Types.Boolean:
			return bool(value)
		else: return value

	def convert_to_storyscript_native_type(self, valtype, value):
		"""
		Returns a Converted to StoryScript version of the value provided to a Type specified.
		[PARAMETER] valtype: Target output type
		[PARAMETER] value: The input value that will be converted.
		[RETURNS] a Converted value. Else the input value If the type is not support yet by the Converter.
		"""
		if valtype == Types.Integer:
			return str(value)
		elif valtype == Types.Float:
			return str(value)
		elif value == Types.String:
			return f"\"{value}\""
		elif value == Types.Boolean:
			if value: return "true"
			else: return "false"
		elif value == Types.Dynamic:
			return f"new Dynamic ({value})"
		else: return value

	def parse_type_from_value(self, value):
		if not isinstance(value, str):
			value = str(value)
		is_float = self.executor.Checkis_float(value)
		if(value.startswith('"') or value.endswith('"')):
			if(not (value.startswith('"') and value.endswith('"'))):
				return Exceptions.InvalidSyntax
			return Types.String
		elif(value == "true" or value == "false"):
			return Types.Boolean
		elif(value.startswith("new List")):
			return Types.List
		elif(value.startswith("new Dictionary")):
			return Types.Dictionary
		elif(value.startswith("new Tuple")):
			return Types.Tuple
		elif(value.startswith("new Dynamic")):
			return Types.Dynamic
		elif(is_float):
			return Types.Float
		elif(not is_float):
			return Types.Integer
		else: return Exceptions.InvalidSyntax

	def parse_type_string(self, string):
		if(string == "bool"):
			return Types.Boolean
		elif(string == "int"):
			return Types.Integer
		elif(string == "float"):
			return Types.Float
		elif(string == "list"):
			return Types.List
		elif(string == "dictionary"):
			return Types.Dictionary
		elif(string == "tuple"):
			return Types.Tuple
		elif(string == "dynamic"):
			return Types.Dynamic
		elif(string == "string"):
			return Types.String
		elif(string == "any"):
			return Types.Any
		else:
			return Exceptions.InvalidSyntax

	def check_naming_violation(self, name):
		""" Returns If the variable naming valid or not """
		if not isinstance(name, str):
			name = str(name)
		if name in ["if", "else", "var", "int",
						"bool", "float", "list", "dictionary",
						"tuple", "const", "override", "func",
						"end", "print", "input", "throw",
						"string", "typeof", "del", "namespace"]:
			return False
		elif name[0] in digits:
			return False
		else: return True

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
		if error: return resl, error

		resr, error = analyse_command_method(expr[operator_index + 1:]) # Analyse the message on the right
		if error: return resr, error

		# Type conversion
		restype = self.parse_type_from_value(resl)
		resl = self.convert_to_python_native_type(restype, resl)
		restype = self.parse_type_from_value(resr)
		resr = self.convert_to_python_native_type(restype, resr)

		if expr[operator_index] == "==": # If the operator was ==
			if resl == resr: return True
		elif expr[operator_index] == ">": # If the operator was >
			if resl > resr: return True
		elif expr[operator_index] == "<": # If the operator was <
			if resl < resr: return True
		elif expr[operator_index] == "!=": # If the operator was !=
			if resl != resr: return True
		elif expr[operator_index] == ">=": # If the operator was >=
			if resl >= resr: return True
		elif expr[operator_index] == "<=": # If the operator was <=
			if resl <= resr: return True
		else: return Exceptions.InvalidSyntax

		return False

	def parse_condition_list(self, expr):
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
			all_var_name = self.executor.symbolTable.GetAllVariableName()
			for i in command:
				if i in all_var_name:
					expr += self.executor.symbolTable.GetVariable(i)[1] + " "
					continue
				expr += i + " "
			res = eval(expr)
			if isinstance(res, str):
				res = f"\"{res}\""
			return res, None
		except NameError as e:
			print("[PYTHON EVALUATION ERROR]")
			return f"NotDefinedException: {e}", Exceptions.NotDefinedException
		except SyntaxError as e:
			print("[PYTHON EVALUATION ERROR]")
			return f"InvalidSyntax: {e}", Exceptions.InvalidSyntax
"""
	[DEPRECATED METHOD]
	def parse_expression(self, command, keep_float=False):
		try:
			isPlus = False
			for i in command:
				if i == "+":
					isPlus = True
			if command[1] == "+" or isPlus:
				res = self.executor.add(command, keep_float)
				if res == Exceptions.InvalidSyntax:
					return None, ("InvalidSyntax: Expected value after + sign\nAt keyword 4", Exceptions.InvalidSyntax)
				return res, None
			elif command[1] == "-":
				res = self.executor.subtract(command, keep_float)
				if res == Exceptions.InvalidSyntax:
					return None, ("InvalidSyntax: Expected numbers after - sign\nAt keyword 4", Exceptions.InvalidSyntax)
				return res, None
			elif command[1] == "*":
				res = self.executor.multiply(command, keep_float)
				if res == Exceptions.InvalidSyntax:
					return None, ("InvalidSyntax: Expected numbers after * sign\nAt keyword 4", Exceptions.InvalidSyntax)
				return res, None
			elif command[1] == "/":
				res = self.executor.divide(command, keep_float)
				if res == Exceptions.InvalidSyntax:
					return None, ("InvalidSyntax: Expected numbers after / sign\nAt keyword 4", Exceptions.InvalidSyntax)
				elif res == Exceptions.DivideByZeroException:
					return None, ("DivideByZeroException: You can't divide numbers with 0", Exceptions.DivideByZeroException)
				return res, None
			elif command[1] == "**":
				res = self.executor.pow(command, keep_float)
				if res == Exceptions.InvalidSyntax:
					return None, ("InvalidSyntax: Expected numbers after ** sign\nAt keyword 4", Exceptions.InvalidSyntax)
				return res, None
			elif command[1] == "%":
				res = self.executor.modulo(command, keep_float)
				if res == Exceptions.InvalidSyntax:
					return None, ("InvalidSyntax: Expected numbers after \% sign", Exceptions.InvalidSyntax)
				return res, None
			else:
				res = ""
				if not isinstance(command, list):
					return command, None
				for i in command:
					res += i + " "
				res = res[:-1]
				return res, None
		except IndexError:
			try:
				return command[0], None
			except IndexError:
				return None, ("InvalidSyntax: Expected numbers after = sign\nAt keyword 2", Exceptions.InvalidSyntax)
"""