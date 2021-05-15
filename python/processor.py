from string import ascii_letters, digits
from langEnums import *

# This class is used to store variables and function
class SymbolTable:
	def __init__(self):
		self.variableTable = {"true":(Types.Boolean, 1), "false":(Types.Boolean, 0)}
		self.functionTable = {}

	def GetAllVariableName(self):
		return self.variableTable.keys()

	def GetVariable(self, key):
		return self.variableTable[key]

	def GetVariableType(self, key):
		return self.variableTable[key][0]

	def GetAllFunctionName(self):
		return self.functionTable.keys()

	def GetFunction(self, key):
		return self.functionTable[key]

	def SetVariable(self, key, value, vartype):
		self.variableTable[key] = (vartype, value)

	def SetFunction(self, key, value, arguments):
		self.functionTable[key] = (arguments, value)

	def DeleteVariable(self, key):
		del self.variableTable[key]

class Executor:
	def __init__(self, symbolTable):
		self.symbolTable = symbolTable

	def CheckIsFloat(self, command):
		isFloat = False
		if(not isinstance(command, str)):
			command = str(command)
		for i in command:
			for j in i:
				if j == ".":
					isFloat = True
					break
		return isFloat

	def add(self, command):
		# Adding numbers.
		isFloat = self.CheckIsFloat(command)

		try:
			try:
				if(isFloat):
					return float(command[0]) + float(command[2])
				else:
					return int(command[0]) + int(command[2])
			except ValueError:
				allvar = self.symbolTable.GetAllVariableName()
				if(command[0].startswith('"')):
					res = ""
					for i in command:
						if i.endswith('"'):
							i = i[:-1]
						if i.startswith('"'):
							i = i[1:]
							res = res[:-1]
						if i == "+":
							continue
						res += i + " "

					res = res[:-1]

					return res
				elif((command[0] in allvar) and (command[2] in allvar)):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0])) or self.CheckIsFloat(self.symbolTable.GetVariable(command[2]))
					if(isFloat):
						return float(self.symbolTable.GetVariable(command[0])[1]) + float(self.symbolTable.GetVariable(command[2])[1])
					else: return int(self.symbolTable.GetVariable(command[0])[1]) + int(self.symbolTable.GetVariable(command[2])[1])
				elif(command[0] in allvar):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0]))
					if(isFloat):
						return float(self.symbolTable.GetVariable(command[0])[1]) + float(command[2])
					else: return int(self.symbolTable.GetVariable(command[0])[1]) + int(command[2])
				elif(command[2] in allvar):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[2]))
					if(isFloat):
						return float(self.symbolTable.GetVariable(command[2])[1]) + float(command[0])
					else: return int(self.symbolTable.GetVariable(command[2])[1]) + int(command[0])
		except IndexError:
			return Exceptions.InvalidSyntax

	def subtract(self, command):
		# Subtract numbers.
		isFloat = self.CheckIsFloat(command)

		try:
			try:
				if(isFloat):
					return float(command[0]) - float(command[2])
				else:
					return int(command[0]) - int(command[2])
			except ValueError:
				allvar = self.symbolTable.GetAllVariableName()
				if((command[0] in allvar) and (command[2] in allvar)):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0])) or self.CheckIsFloat(self.symbolTable.GetVariable(command[2]))
					if(isFloat):
						return float(self.symbolTable.GetVariable(command[0])[1]) - float(self.symbolTable.GetVariable(command[2])[1])
					else: return int(self.symbolTable.GetVariable(command[0])[1]) - int(self.symbolTable.GetVariable(command[2])[1])
				elif(command[0] in allvar):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0])) or isFloat
					if(isFloat):
						return float(self.symbolTable.GetVariable(command[0])[1]) - float(command[2])
					else: return int(self.symbolTable.GetVariable(command[0])[1]) - int(command[2])
				elif(command[2] in allvar):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[2])) or isFloat
					if(isFloat):
						return float(self.symbolTable.GetVariable(command[2])[1]) - float(command[0])
					else: return int(self.symbolTable.GetVariable(command[2])[1]) - int(command[0])
		except IndexError:
			return Exceptions.InvalidSyntax

	def multiply(self, command):
		isFloat = self.CheckIsFloat(command)

		try:
			try:
				# If both are normal numbers (Not variable)
				if(isFloat):
					return float(command[0]) * float(command[2])
				else:
					return int(command[0]) * int(command[2])
			except ValueError:
				allvar = self.symbolTable.GetAllVariableName()
				if((command[0] in allvar) and (command[2] in allvar)):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0])) or self.CheckIsFloat(self.symbolTable.GetVariable(command[2]))
					if(isFloat):
						return float(self.symbolTable.GetVariable(command[0])[1]) * float(self.symbolTable.GetVariable(command[2])[1])
					else: return int(self.symbolTable.GetVariable(command[0])[1]) * int(self.symbolTable.GetVariable(command[2])[1])
				elif(command[0] in allvar):
					# Incase the First is variable and the second is not
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0])) or isFloat
					if(isFloat):
						return float(self.symbolTable.GetVariable(command[0])[1]) * float(command[2])
					else: return int(self.symbolTable.GetVariable(command[0])[1]) * int(command[2])
				elif(command[2] in allvar):
					# Incase the First is not variable and the second is a variable
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[2])) or isFloat
					if(isFloat):
						return float(self.symbolTable.GetVariable(command[2])[1]) * float(command[0])
					else: return int(self.symbolTable.GetVariable(command[2])[1]) * int(command[0])
		except IndexError:
			return Exceptions.InvalidSyntax

	def divide(self, command):
		isFloat = self.CheckIsFloat(command)

		try:
			try:
				if(isFloat):
					return float(command[0]) / float(command[2])
				else:
					return int(command[0]) / int(command[2])
			except ValueError:
				allvar = self.symbolTable.GetAllVariableName()
				if((command[0] in allvar) and (command[2] in allvar)):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0])) or self.CheckIsFloat(self.symbolTable.GetVariable(command[2]))
					if(isFloat):
						return float(self.symbolTable.GetVariable(command[0])[1]) / float(self.symbolTable.GetVariable(command[2])[1])
					else: return int(self.symbolTable.GetVariable(command[0])[1]) / int(self.symbolTable.GetVariable(command[2])[1])
				elif(command[0] in allvar):
					# Incase the First is variable and the second is not
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0])) or isFloat
					if(isFloat):
						return float(self.symbolTable.GetVariable(command[0])[1]) / float(command[2])
					else: return int(self.symbolTable.GetVariable(command[0])[1]) / int(command[2])
				elif(command[2] in allvar):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[2])) or isFloat
					if(isFloat):
						return float(self.symbolTable.GetVariable(command[2])[1]) / float(command[0])
					else: return int(self.symbolTable.GetVariable(command[2])[1]) / int(command[0])
		except IndexError:
			return Exceptions.InvalidSyntax
		except ZeroDivisionError:
			return Exceptions.DivideByZeroException

	def pow(self, command):
		isFloat = self.CheckIsFloat(command)

		try:
			try:
				if(isFloat):
					return float(command[0]) ** float(command[2])
				else:
					return int(command[0]) ** int(command[2])
			except ValueError:
				allvar = self.symbolTable.GetAllVariableName()
				if((command[0] in allvar) and (command[2] in allvar)):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0])) or self.CheckIsFloat(self.symbolTable.GetVariable(command[2]))
					if(isFloat):
						return float(self.symbolTable.GetVariable(command[0])[1]) ** float(self.symbolTable.GetVariable(command[2])[1])
					else: return int(self.symbolTable.GetVariable(command[0])[1]) ** int(self.symbolTable.GetVariable(command[2])[1])
				elif(command[0] in allvar):
					# Incase the First is variable and the second is not
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0])) or isFloat
					if(isFloat):
						return float(self.symbolTable.GetVariable(command[0])[1]) ** float(command[2])
					else: return int(self.symbolTable.GetVariable(command[0])[1]) ** int(command[2])
				elif(command[2] in allvar):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[2])) or isFloat
					if(isFloat):
						return float(self.symbolTable.GetVariable(command[2])[1]) ** float(command[0])
					else: return int(self.symbolTable.GetVariable(command[2])[1]) ** int(command[0])
		except IndexError:
			return Exceptions.InvalidSyntax

class Parser:
	def __init__(self, executor):
		self.executor = executor
		pass

	def ParseEscapeCharacter(self, trimmedString):
		escapeChar = ""
		isEscapeCharDetected = False
		outstr = ""
		for i in trimmedString:
			outchar = i
			if i == "\\":
				isEscapeCharDetected = True
				outchar += outstr
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

	def ParseTypeFromValue(self, value):
		if not isinstance(value, str):
			value = str(value)
		isFloat = self.executor.CheckIsFloat(value)
		if(value.startswith('"') and value.endswith('"')):
			return Types.String
		elif(isFloat):
			return Types.Float
		elif(not isFloat):
			return Types.Integer
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

	# Returns If the value valid or not
	def CheckNamingViolation(self, name):
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

	def ParseExpression(self, command, executor):
		try:
			isPlus = False
			for i in command:
				if i == "+":
					isPlus = True
			if command[1] == "+" or isPlus:
				res = executor.add(command)
				if res == Exceptions.InvalidSyntax:
					return None, ("InvalidSyntax: Expected value after + sign\nAt keyword 4", Exceptions.InvalidSyntax)
				return res, None
			elif command[1] == "-":
				res = executor.subtract(command)
				if res == Exceptions.InvalidSyntax:
					return None, ("InvalidSyntax: Expected numbers after - sign\nAt keyword 4", Exceptions.InvalidSyntax)
				return res, None
			elif command[1] == "*":
				res = executor.multiply(command)
				if res == Exceptions.InvalidSyntax:
					return None, ("InvalidSyntax: Expected numbers after * sign\nAt keyword 4", Exceptions.InvalidSyntax)
				return res, None
			elif command[1] == "/":
				res = executor.divide(command)
				if res == Exceptions.InvalidSyntax:
					return None, ("InvalidSyntax: Expected numbers after / sign\nAt keyword 4", Exceptions.InvalidSyntax)
				elif res == Exceptions.DivideByZeroException:
					return None, ("DivideByZeroException: You can't divide numbers with 0", Exceptions.DivideByZeroException)
				return res, None
			elif command[1] == "**":
				res = executor.pow(command)
				if res == Exceptions.InvalidSyntax:
					return None, ("InvalidSyntax: Expected numbers after ** sign\nAt keyword 4", Exceptions.InvalidSyntax)
				return res, None
			else:
				res = ""
				for i in command:
					res += i + " "
				res = res[:-1]
				return res, None
		except IndexError:
			try:
				return command[0], None
			except IndexError:
				return None, ("InvalidSyntax: Expected numbers after = sign\nAt keyword 2", Exceptions.InvalidSyntax)

class Lexer:
	def __init__(self, trimmedCommand, symbolTable, executor=None, parser=None):
		self.command = trimmedCommand
		self.executor = executor
		self.symbolTable = symbolTable
		self.parser = parser

		if executor == None:
			self.executor = Executor(self.symbolTable)

		if parser == None:
			self.parser = Parser(self.executor)

	def analyseCommand(self):
		tc = self.command
		isMultipleCommands = False
		multipleCommandsIndex = -1
		# All Keywords
		basekeywords = ["if", "else", "var", "int",
						"bool", "float", "list", "dictionary",
						"tuple", "const", "override", "func",
						"end", "print", "input", "throw",
						"string", "typeof", "del", "namespace"]

		for i in tc:
			multipleCommandsIndex += 1
			if i == "&&":
				isMultipleCommands = True
				break

		allVariableName = self.symbolTable.GetAllVariableName()
		allFunctionName = self.symbolTable.GetAllFunctionName()

		if tc[0] in allVariableName:
			try:
				if tc[1] == "=":
					res, error = self.parser.ParseExpression(tc[2:multipleCommandsIndex + 1], self.executor)
					if error: return error[0], error[1]
					value = ""
					try:
						if tc[2] in allVariableName:
							tc[2] = (self.symbolTable.GetVariable(tc[2]))[1]
						if tc[4] in allVariableName:
							tc[4] = (self.symbolTable.GetVariable(tc[4]))[1]
					except IndexError:
						pass

					for i in tc[2:multipleCommandsIndex + 1]:
						value += i + " "
					value = value[:-1]

					valtype = self.parser.ParseTypeFromValue(value)
					if valtype == Exceptions.InvalidSyntax:
						return "InvalidValue: Invalid value", Exceptions.InvalidValue
					vartype = self.symbolTable.GetVariableType(tc[0])
					# Check if Value Type matches Variable type
					if valtype != vartype:
						return "InvalidValue: Value doesn't match variable type.", Exceptions.InvalidValue
					res = msg = self.parser.ParseEscapeCharacter(res)
					error = self.symbolTable.SetVariable(tc[0], res, vartype)
					if error: return error[0], error[1]
					return None, None
				else:
					res, error = self.parser.ParseExpression(tc[0:multipleCommandsIndex + 1], self.executor)
					if error: return error[0], error[1]
					return res, None
			except IndexError:
				return self.symbolTable.GetVariable(tc[0])[1], None
		elif tc[0] in basekeywords:
			if tc[0] in ["var", "int", "bool", "float", "list", "dictionary", "tuple", "const", "string"]:
				try:
					if(tc[1] in self.symbolTable.GetAllVariableName()):
						return f"AlreadyDefined: a Variable {tc[1]} is already defined", Exceptions.AlreadyDefined
					
					# Checking for variable naming violation
					if(tc[1][0] in digits):
						return "InvalidValue: a Variable name cannot start with digits.", Exceptions.InvalidValue

					# var(0) a(1) =(2) 3(3)
					res, error = self.parser.ParseExpression(tc[3:multipleCommandsIndex + 1], self.executor)
					if error: return error[0], error[1]
					value = ""

					try:
						if tc[3] in allVariableName:
							tc[3] = (self.symbolTable.GetVariable(tc[3]))[1]
						if tc[5] in allVariableName:
							tc[5] = (self.symbolTable.GetVariable(tc[5]))[1]
					except IndexError:
						pass

					for i in tc[3:multipleCommandsIndex + 1]:
						value += i + " "
					value = value[:-1]
					vartype = self.parser.ParseTypeFromValue(value)
					if tc[0] != "var":
						definedType = self.parser.ParseTypeString(tc[0])
						# Check If existing variable type matches the New value type
						if definedType != vartype:
							return "InvalidValue: Variable types doesn't match value type.", Exceptions.InvalidValue
					if vartype == Exceptions.InvalidSyntax:
						return "InvalidSyntax: Invalid value", Exceptions.InvalidSyntax
					res = msg = self.parser.ParseEscapeCharacter(res)
					error = self.symbolTable.SetVariable(tc[1], res, vartype)
					if error: return error[0], error[1]
					return None, None
				except IndexError:
					# var(0) a(1)
					if tc[0] == "var":
						return "InvalidSyntax: Initial value needed for var keyword", Exceptions.InvalidSyntax
					vartype = self.parser.ParseTypeString(tc[0])
					if vartype == Exceptions.InvalidSyntax:
						return "InvalidSyntax: Invalid type", Exceptions.InvalidSyntax
					self.symbolTable.SetVariable(tc[1], None, vartype)
					return None, None
			elif tc[0] == "print":
				value = ""
				for i in tc[1:multipleCommandsIndex + 1]:
					value += i + " "
				value = value[:-1]
				if not value.startswith('('):
					return "InvalidSyntax: Parenthesis is needed after a function name", Exceptions.InvalidSyntax
				if not value.endswith(')'):
					return "InvalidSyntax: Parenthesis is needed after an Argument input", Exceptions.InvalidSyntax
				value = value[1:-1]
				svalue = value.split()
				value, error = self.parser.ParseExpression(svalue, self.executor)
				if value in allVariableName:
					value = self.symbolTable.GetVariable(value)[1]
				value = str(value)
				if value.startswith('"'):
					value = value[1:]
				if value.endswith('"'):
					value = value[:-1]
				if error: return error[0], error[1]
				return value, None
			elif tc[0] == "throw":
				# Throw keyword. "throw [Exception] [Description]"
				if(tc[1] == "InvalidSyntax"):
					try:
						if(tc[2: multipleCommandsIndex + 1]):
							msg = ""
							for i in tc[2:multipleCommandsIndex + 1]:
								if i.startswith('"'):
									i = i[1:]
								if i.endswith('"'):
									i = i[:-1]
								msg += i + " "
							msg = msg[:-1]
							msg = self.parser.ParseEscapeCharacter(msg)
							return f"InvalidSyntax: {msg}", Exceptions.InvalidSyntax
						else: raise IndexError
					except IndexError:
						return "InvalidSyntax: No Description provided", Exceptions.InvalidSyntax
				elif(tc[1] == "AlreadyDefined"):
					try:
						if(tc[2:multipleCommandsIndex + 1]):
							msg = ""
							for i in tc[2:multipleCommandsIndex + 1]:
								if i.startswith('"'):
									i = i[1:]
								if i.endswith('"'):
									i = i[:-1]
								msg += i + " "
							msg = msg[:-1]
							msg = self.parser.ParseEscapeCharacter(msg)
							return f"AlreadyDefined: {msg}", Exceptions.AlreadyDefined
						else: raise IndexError
					except IndexError:
						return "AlreadyDefined: No Description provided", Exceptions.AlreadyDefined
				elif(tc[1] == "NotImplementedException"):
					try:
						if(tc[2:multipleCommandsIndex + 1]):
							msg = ""
							for i in tc[2:multipleCommandsIndex + 1]:
								if i.startswith('"'):
									i = i[1:]
								if i.endswith('"'):
									i = i[:-1]
								msg += i + " "
							msg = msg[:-1]
							msg = self.parser.ParseEscapeCharacter(msg)
							return f"NotImplementedException: {msg}", Exceptions.NotImplementedException
						else: raise IndexError
					except IndexError:
						return "NotImplementedException: This feature is not implemented", Exceptions.NotImplementedException
				elif(tc[1] == "NotDefinedException"):
					try:
						if(tc[2:multipleCommandsIndex + 1]):
							msg = ""
							for i in tc[2:multipleCommandsIndex + 1]:
								if i.startswith('"'):
									i = i[1:]
								if i.endswith('"'):
									i = i[:-1]
								msg += i + " "
							msg = msg[:-1]
							msg = self.parser.ParseEscapeCharacter(msg)
							return f"NotDefinedException: {msg}", Exceptions.NotDefinedException
						else: raise IndexError
					except IndexError:
						return "NotDefinedException: No Description provided", Exceptions.NotDefinedException
				elif(tc[1] == "DivideByZeroException"):
					try:
						if(tc[2:multipleCommandsIndex + 1]):
							msg = ""
							for i in tc[2:multipleCommandsIndex + 1]:
								if i.startswith('"'):
									i = i[1:]
								if i.endswith('"'):
									i = i[:-1]
								msg += i + " "
							msg = msg[:-1]
							msg = self.parser.ParseEscapeCharacter(msg)
							return f"DivideByZeroException: {msg}", Exceptions.DivideByZeroException
						else: raise IndexError
					except IndexError:
						return "DivideByZeroException: You cannot divide numbers with 0", Exceptions.DivideByZeroException
				elif(tc[1] == "InvalidValue"):
					try:
						if(tc[2:multipleCommandsIndex + 1]):
							msg = ""
							for i in tc[2:multipleCommandsIndex + 1]:
								if i.startswith('"'):
									i = i[1:]
								if i.endswith('"'):
									i = i[:-1]
								msg += i + " "
							msg = msg[:-1]
							msg = self.parser.ParseEscapeCharacter(msg)
							return f"InvalidValue: {msg}", Exceptions.InvalidValue
						else: raise IndexError
					except IndexError:
						return "InvalidValue: No Description provided", Exceptions.InvalidValue
				elif(tc[1] == "InvalidTypeException"):
					try:
						if(tc[2:multipleCommandsIndex + 1]):
							msg = ""
							for i in tc[2:multipleCommandsIndex + 1]:
								if i.startswith('"'):
									i = i[1:]
								if i.endswith('"'):
									i = i[:-1]
								msg += i + " "
							msg = msg[:-1]
							msg = self.parser.ParseEscapeCharacter(msg)
							return f"InvalidTypeException: {msg}", Exceptions.InvalidTypeException
						else: raise IndexError
					except IndexError:
						return "InvalidTypeException: No Description provided", Exceptions.InvalidTypeException
				else:
					return "InvalidValue: The Exception entered is not defined", Exceptions.InvalidValue
			elif tc[0] == "typeof":
				if tc[1].startswith('('):
					tc[1] = tc[1][1:]
				else: return "InvalidSyntax: Parenthesis is needed after a function name", Exceptions.InvalidSyntax
				if tc[multipleCommandsIndex].endswith(')'):
					tc[multipleCommandsIndex] = tc[multipleCommandsIndex][:-1]
				else: return "InvalidSyntax: Parenthesis is needed after an Argument input", Exceptions.InvalidSyntax
				if(tc[1] in allVariableName):
					return self.symbolTable.GetVariableType(tc[1]), None
				res, error = self.parser.ParseExpression(tc[1:multipleCommandsIndex + 1], self.executor)
				if error: return error[0], error[1]
				if(not tc[1] in allVariableName and tc[1][0] in ascii_letters):
					return f"InvalidValue: {tc[1]} is not a Variable and Is not a String.", Exceptions.InvalidValue
				res = self.parser.ParseTypeFromValue(res)
				return res, None
			elif tc[0] == "del":
				if tc[1] in allVariableName:
					self.symbolTable.DeleteVariable(tc[1])
					return None, None
				else:
					return "InvalidValue: The Input is not a variable.", Exceptions.InvalidValue
			elif tc[0] == "func":
				# func[0] Name[1] (arguments)[2]
				endIndex = -1
				for i in tc:
					endIndex += 1
					if i == "end":
						break

				if not tc[1] == "override":
					if tc[1] in allFunctionName:
						return f"AlreadyDefined: The {tc[1]} function is already defined.", Exceptions.AlreadyDefined
				else:
					# func[0] override[1] Name[2] (arguments)[3]
					argumentsEndIndex = 1
					for i in tc[2:endIndex]:
						argumentsEndIndex += 1
						if i == ")":
							break
					if not tc[2] in allFunctionName:
						return f"NotDefinedException: The {tc[2]} function is not defined. You can't override non-existed function.", Exceptions.AlreadyDefined
					else: self.symbolTable.SetFunction(tc[2], tc[argumentsEndIndex:endIndex], tc[3:argumentsEndIndex - 1])
				# Find all arguments declared.
				argumentsEndIndex = 0
				arguments = []
				# isConstantsKeyword = False
				isTypesKeywordFound = False
				for i in tc[2:endIndex]:
					argumentsEndIndex += 1
					trimmedVal = ""
					if i.startswith('('):
						trimmedVal = i[1:]
					if i.endswith(","):
						trimmedVal = i[:-1]
					if i.endswith(")"):
						trimmedVal = i[:-1]
					print(trimmedVal)
					if trimmedVal in ["any", "int", "bool", "float", "list", "dictionary", "tuple", "const", "string"]:
						# if i == "const":
						isTypesKeywordFound = trimmedVal
						continue
					if isTypesKeywordFound:
						if not self.parser.CheckNamingViolation(trimmedVal):
							return "InvalidValue: Variable naming violation.", Exceptions.InvalidValue
						outtype = self.parser.ParseTypeString(isTypesKeywordFound)
						if outtype == Exceptions.InvalidSyntax:
							return "InvalidValue: Invalid Variable type.", Exceptions.InvalidValue
						arguments.append((outtype, i))
						isTypesKeywordFound = False
				self.symbolTable.SetFunction(tc[1], tc[argumentsEndIndex:endIndex], arguments)
				return None, None
			else:
				return "NotImplementedException: This feature is not implemented", Exceptions.NotImplementedException
		elif tc[0] in allFunctionName:
			customSymbolTable = self.symbolTable
			functionObject = self.symbolTable.GetFunction(tc[0])
			# Loops through all arguments
			currentArgumentsIndex = 0
			if functionObject[0] != ():
				for i in functionObject[0]:
					currentArgumentsIndex += 1
					try:
						if tc[currentArgumentsIndex].startswith('('):
							tc[currentArgumentsIndex] = tc[currentArgumentsIndex][1:]
						if tc[currentArgumentsIndex].endswith(')'):
							tc[currentArgumentsIndex] = tc[currentArgumentsIndex][:-1]
						tc[currentArgumentsIndex]
						vartype = i[0]
						valtype = self.parser.ParseTypeFromValue(tc[currentArgumentsIndex])
						print(tc[currentArgumentsIndex], valtype)
						if vartype != valtype:
							if vartype != Types.Any:
								return "InvalidTypeException: Value type doesn't match required type.", Exceptions.InvalidTypeException
						customSymbolTable.SetVariable(i[1], tc[currentArgumentsIndex], vartype)
					except IndexError:
						return "NotDefinedException: The argument required is not all entered.", Exceptions.NotDefinedException
			print(functionObject, customSymbolTable.GetAllVariableName())
			flex = Lexer(functionObject[1], customSymbolTable, self.executor, self.parser)
			res, error = flex.analyseCommand()
			return res, error
		else:
			res, error = self.parser.ParseExpression(tc[0:multipleCommandsIndex + 1], self.executor)
			if(error): return error[0], error[1]
			return res, None

GlobalVariableTable = SymbolTable()

def execute(command):
	trimmedCommand = command.split()

	lexer = Lexer(trimmedCommand, GlobalVariableTable)
	res, error = lexer.analyseCommand()

	return res

def parseFile(fileName):
	f = open(fileName, "r")
	lines = f.readlines()
	for i in lines:
		i = i.split()
	for i in lines:
		lexer = Lexer(trimmedCommand, GlobalVariableTable)
		res, error = lexer.analyseCommand()
		if res != None:
			print(res)