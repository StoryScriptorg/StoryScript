from string import ascii_letters, digits
from langEnums import *

class Parser:
	def __init__(self, executor):
		self.executor = executor
		pass

	def ParseEscapeCharacter(self, trimmedString):
		escapeChar = ""
		isEscapeCharDetected = False
		outstr = ""
		for i in str(trimmedString):
			outchar = i
			if i == "\\":
				isEscapeCharDetected = True
				continue
			if isEscapeCharDetected:
				isEscapeCharDetected = False
				if i == "n":
					outchar = "\n"
				elif i == "\\":
					pass
				elif i == "t":
					outchar = "\t"
			outstr += outchar
		return outstr

	def ParseStringList(self, command):
		res = ""
		for i in command:
			res += i + " "
		res = res[:-1]
		return res

	def convertToPythonNativeType(self, valtype, value):
		if valtype == Types.Integer:
			return int(value)
		elif valtype == Types.Float:
			return float(value)
		elif value == Types.String:
			return str(value)
		elif value == Types.Boolean:
			return bool(value)
		else: return value

	def ParseTypeFromValue(self, value):
		if not isinstance(value, str):
			value = str(value)
		isFloat = self.executor.CheckIsFloat(value)
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
		elif(isFloat):
			return Types.Float
		elif(not isFloat):
			return Types.Integer
		else: return Exceptions.InvalidSyntax

	def ParseTypeString(self, string):
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

	def CheckNamingViolation(self, name):
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

	def ParseConditionExpression(self, expr, analyseCommandMethod):
		""" Parse If the condition is True or False """
		# [:OperatorIndex] = Accessing a Message before the operator
		# [OperatorIndex + 1:] = Accessing a Message after the operator
		operatorIndex = 0
		for i in expr:
			if i in [">", "<", "==", "!=", ">=", "<="]:
				break
			operatorIndex += 1
		resl, error = analyseCommandMethod(expr[:operatorIndex]) # Analyse the message on the left
		if error: return resl, error

		resr, error = analyseCommandMethod(expr[operatorIndex + 1:]) # Analyse the message on the right
		if error: return resr, error

		# Type conversion
		restype = self.ParseTypeFromValue(resl)
		resl = self.convertToPythonNativeType(restype, resl)
		restype = self.ParseTypeFromValue(resr)
		resr = self.convertToPythonNativeType(restype, resr)

		if expr[operatorIndex] == "==": # If the operator was ==
			if resl == resr: return True
		elif expr[operatorIndex] == ">": # If the operator was >
			if resl > resr: return True
		elif expr[operatorIndex] == "<": # If the operator was <
			if resl < resr: return True
		elif expr[operatorIndex] == "!=": # If the operator was !=
			if resl != resr: return True
		elif expr[operatorIndex] == ">=": # If the operator was >=
			if resl >= resr: return True
		elif expr[operatorIndex] == "<=": # If the operator was <=
			if resl <= resr: return True
		else: return Exceptions.InvalidSyntax

		return False

	def ParseConditions(self, expr):
		""" Separate expressions into a list of conditions """
		conditionslist:list = [] # List of conditions
		conditions:list = [] # List of condition
		condition:list = [] # Condition
		currentConditionType = ConditionType.Single # Current condition type
		for i in expr:
			if i == "and":
				if currentConditionType != ConditionType.Single:
					conditions.append(condition)
					conditions.append(currentConditionType)
					conditionslist.append(conditions)
					conditions = []
					condition = []
				conditions.append(condition)
				condition = []
				currentConditionType = ConditionType.And
				continue
			if i == "or":
				if currentConditionType != ConditionType.Single:
					conditions.append(condition)
					conditions.append(currentConditionType)
					conditionslist.append(conditions)
					conditions = []
					condition = []
				conditions.append(condition)
				condition = []
				currentConditionType = ConditionType.Or
				continue
			if i == "then":
				conditions.append(condition)
				conditions.append(currentConditionType)
				conditionslist.append(conditions)
				conditions = []
				condition = []
				break
			condition.append(i)
		return conditionslist

	def ParseExpression(self, command, keepFloat=False):
		try:
			isPlus = False
			for i in command:
				if i == "+":
					isPlus = True
			if command[1] == "+" or isPlus:
				res = self.executor.add(command, keepFloat)
				if res == Exceptions.InvalidSyntax:
					return None, ("InvalidSyntax: Expected value after + sign\nAt keyword 4", Exceptions.InvalidSyntax)
				return res, None
			elif command[1] == "-":
				res = self.executor.subtract(command, keepFloat)
				if res == Exceptions.InvalidSyntax:
					return None, ("InvalidSyntax: Expected numbers after - sign\nAt keyword 4", Exceptions.InvalidSyntax)
				return res, None
			elif command[1] == "*":
				res = self.executor.multiply(command, keepFloat)
				if res == Exceptions.InvalidSyntax:
					return None, ("InvalidSyntax: Expected numbers after * sign\nAt keyword 4", Exceptions.InvalidSyntax)
				return res, None
			elif command[1] == "/":
				res = self.executor.divide(command, keepFloat)
				if res == Exceptions.InvalidSyntax:
					return None, ("InvalidSyntax: Expected numbers after / sign\nAt keyword 4", Exceptions.InvalidSyntax)
				elif res == Exceptions.DivideByZeroException:
					return None, ("DivideByZeroException: You can't divide numbers with 0", Exceptions.DivideByZeroException)
				return res, None
			elif command[1] == "**":
				res = self.executor.pow(command, keepFloat)
				if res == Exceptions.InvalidSyntax:
					return None, ("InvalidSyntax: Expected numbers after ** sign\nAt keyword 4", Exceptions.InvalidSyntax)
				return res, None
			elif command[1] == "%":
				res = self.executor.modulo(command, keepFloat)
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
