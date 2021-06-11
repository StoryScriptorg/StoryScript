from langParser import Parser
from executor import Executor
from langEnums import *

# This class is used to store variables and function
class SymbolTable:
	def __init__(self):
		self.variableTable = {"true":(Types.Boolean, 1), "false":(Types.Boolean, 0)}
		self.functionTable = {}
		self.enableFunctionFeature = False

	def copyvalue(self):
		return self.variableTable, self.functionTable, self.enableFunctionFeature

	def importdata(self, variableTable, functionTable, enableFunctionFeature):
		self.variableTable = variableTable
		self.functionTable = functionTable
		self.enableFunctionFeature = enableFunctionFeature

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

	def DeleteFunction(self, key):
		del self.functionTable[key]

class Lexer:
	def __init__(self, symbolTable, executor=None, parser=None):
		self.executor = executor
		self.symbolTable = symbolTable
		self.parser = parser

		if executor == None:
			self.executor = Executor(self.symbolTable)

		if parser == None:
			self.parser = Parser(self.executor)

	def throwKeyword(self, tc, multipleCommandsIndex):
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

	def analyseCommand(self, tc):
		isMultipleCommands = False
		multipleCommandsIndex = -1
		# All Keywords
		basekeywords = ["if", "else", "var", "int",
						"bool", "float", "list", "dictionary",
						"tuple", "const", "override", "func",
						"end", "print", "input", "throw",
						"string", "typeof", "del", "namespace",
						"#define", "dynamic", "loopfor", "switch",
						"input", "exit"]

		for i in tc:
			multipleCommandsIndex += 1
			if i == "&&":
				isMultipleCommands = True
				break

		allVariableName = self.symbolTable.GetAllVariableName()
		allFunctionName = self.symbolTable.GetAllFunctionName()

		if tc[0] in allVariableName:
			try:
				if tc[1] == "=": # Set operator
					res, error = self.analyseCommand(tc[2:multipleCommandsIndex + 1])
					if error: return res, error
					value = ""

					for i in tc[2:multipleCommandsIndex + 1]:
						value += i + " "
					value = value[:-1]

					valtype = self.parser.ParseTypeFromValue(res)
					if valtype == Exceptions.InvalidSyntax:
						return "InvalidValue: Invalid value", Exceptions.InvalidValue
					vartype = self.symbolTable.GetVariableType(tc[0])
					# Check if Value Type matches Variable type
					if valtype != vartype:
						return "InvalidValue: Value doesn't match variable type.", Exceptions.InvalidValue
					res = self.parser.ParseEscapeCharacter(res)
					if res in allVariableName:
						res = (self.symbolTable.GetVariable(res))[1]
					error = self.symbolTable.SetVariable(tc[0], res, vartype)
					if error: return error[0], error[1]
					return None, None
				elif tc[1] == "+=": # Add & Set operator
					vartype = self.symbolTable.GetVariableType(tc[0])
					keepFloat = False
					if vartype == Types.Float:
						keepFloat = True
					res, error = self.analyseCommand(tc[2:multipleCommandsIndex + 1])
					if error: return res, error
					res, error = self.parser.ParseExpression([tc[0], "+", str(res)], keepFloat)
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

					valtype = self.parser.ParseTypeFromValue(res)
					if valtype == Exceptions.InvalidSyntax:
						return "InvalidValue: Invalid value", Exceptions.InvalidValue

					# Check if Value Type matches Variable type
					if valtype != vartype:
						return "InvalidValue: Value doesn't match variable type.", Exceptions.InvalidValue
					res = self.parser.ParseEscapeCharacter(res)
					error = self.symbolTable.SetVariable(tc[0], res, vartype)
					if error: return error[0], error[1]
					return None, None
				elif tc[1] == "-=": # Subtract & Set operator
					vartype = self.symbolTable.GetVariableType(tc[0])
					keepFloat = False
					if vartype == Types.Float:
						keepFloat = True
					res, error = self.parser.ParseExpression(tc[2:multipleCommandsIndex + 1], keepFloat)
					if error: return error[0], error[1]
					res, error = self.parser.ParseExpression([tc[0], "-", str(res)], keepFloat)
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

					valtype = self.parser.ParseTypeFromValue(res)
					if valtype == Exceptions.InvalidSyntax:
						return "InvalidValue: Invalid value", Exceptions.InvalidValue

					# Check if Value Type matches Variable type
					if valtype != vartype:
						return "InvalidValue: Value doesn't match variable type.", Exceptions.InvalidValue
					res = self.parser.ParseEscapeCharacter(res)
					error = self.symbolTable.SetVariable(tc[0], res, vartype)
					if error: return error[0], error[1]
					return None, None
				elif tc[1] == "*=": # Multiply & Set operator
					vartype = self.symbolTable.GetVariableType(tc[0])
					keepFloat = False
					if vartype == Types.Float:
						keepFloat = True
					res, error = self.parser.ParseExpression(tc[2:multipleCommandsIndex + 1], keepFloat)
					if error: return error[0], error[1]
					res, error = self.parser.ParseExpression([tc[0], "*", str(res)], keepFloat)
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

					valtype = self.parser.ParseTypeFromValue(res)
					if valtype == Exceptions.InvalidSyntax:
						return "InvalidValue: Invalid value", Exceptions.InvalidValue

					# Check if Value Type matches Variable type
					if valtype != vartype:
						return "InvalidValue: Value doesn't match variable type.", Exceptions.InvalidValue
					res = self.parser.ParseEscapeCharacter(res)
					error = self.symbolTable.SetVariable(tc[0], res, vartype)
					if error: return error[0], error[1]
					return None, None
				elif tc[1] == "/=": # Divide & Set operator
					vartype = self.symbolTable.GetVariableType(tc[0])
					keepFloat = False
					if vartype == Types.Float:
						keepFloat = True
					res, error = self.parser.ParseExpression(tc[2:multipleCommandsIndex + 1], keepFloat)
					if error: return error[0], error[1]
					res, error = self.parser.ParseExpression([tc[0], "/", str(res)], keepFloat)
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

					valtype = self.parser.ParseTypeFromValue(res)
					if valtype == Exceptions.InvalidSyntax:
						return "InvalidValue: Invalid value", Exceptions.InvalidValue

					# Check if Value Type matches Variable type
					if valtype != vartype:
						return "InvalidValue: Value doesn't match variable type.", Exceptions.InvalidValue
					res = self.parser.ParseEscapeCharacter(res)
					error = self.symbolTable.SetVariable(tc[0], res, vartype)
					if error: return error[0], error[1]
					return None, None
				elif tc[1] == "%=": # Modulo Operaion & Set operator
					vartype = self.symbolTable.GetVariableType(tc[0])
					keepFloat = False
					if vartype == Types.Float:
						keepFloat = True
					res, error = self.analyseCommand(tc[2:multipleCommandsIndex + 1])
					if error: return res, error
					res, error = self.parser.ParseExpression([tc[0], "%", str(res)], keepFloat)
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

					valtype = self.parser.ParseTypeFromValue(res)
					if valtype == Exceptions.InvalidSyntax:
						return "InvalidValue: Invalid value", Exceptions.InvalidValue

					# Check if Value Type matches Variable type
					if valtype != vartype:
						return "InvalidValue: Value doesn't match variable type.", Exceptions.InvalidValue
					res = self.parser.ParseEscapeCharacter(res)
					error = self.symbolTable.SetVariable(tc[0], res, vartype)
					if error: return error[0], error[1]
					return None, None
				else:
					res, error = self.parser.ParseExpression(tc[0:multipleCommandsIndex + 1])
					if error: return error[0], error[1]
					return res, None
			except IndexError:
				var = self.symbolTable.GetVariable(tc[0])[1]
				if var.startswith("new Dynamic ("):
					var = var.removeprefix("new Dynamic (")
					if var.endswith(')'):
						var = var[:-1]
				return var, None
		elif tc[0] in basekeywords:
			if tc[0] in ["var", "int", "bool", "float", "list", "dictionary", "tuple", "const", "string", "dynamic"]:
				try:
					definedType = self.parser.ParseTypeString(tc[0])
					if(tc[1] in self.symbolTable.GetAllVariableName()):
						return f"AlreadyDefined: a Variable {tc[1]} is already defined", Exceptions.AlreadyDefined
					
					# Checking for variable naming violation
					if not (self.parser.CheckNamingViolation(tc[1])):
						return "InvalidValue: a Variable name cannot start with digits.", Exceptions.InvalidValue

					# Check If to Keep the Float in the Calculation or not
					keepFloat = False
					if definedType == Types.Float:
						keepFloat = True

					# var(0) a(1) =(2) 3(3)
					res, error = self.analyseCommand(tc[3:multipleCommandsIndex + 1])
					if error: return res, error
					value = ""

					for i in tc[3:multipleCommandsIndex + 1]:
						value += i + " "
					value = value[:-1]
					vartype = self.parser.ParseTypeFromValue(res)
					if tc[0] != "var":
						# Check If existing variable type matches the New value type
						if definedType != vartype:
							return "InvalidValue: Variable types doesn't match value type.", Exceptions.InvalidValue
					if vartype == Exceptions.InvalidSyntax:
						return "InvalidSyntax: Invalid value", Exceptions.InvalidSyntax
					if value.startswith("new Dynamic ("):
						msg = value[13:]
						if value.endswith(')'):
							msg = msg[:-1]
						res, error = self.parser.ParseExpression(msg.split())
						if error: return error[0], error[1]
						res = "new Dynamic (" + str(res) + ")"
					res = self.parser.ParseEscapeCharacter(res)
					if res in allVariableName:
						res = self.symbolTable.GetVariable(res)[1]
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
				if not value.startswith('('): # Check If the expression has parentheses around or not
					return "InvalidSyntax: Parenthesis is needed after a function name", Exceptions.InvalidSyntax # Return error if not exists
				if not value.endswith(')'): # Check If the expression has parentheses around or not
					return "InvalidSyntax: Parenthesis is needed after an Argument input", Exceptions.InvalidSyntax # Return error if not exists
				value = value[1:-1]
				svalue = value.split()
				res, error = self.analyseCommand(svalue)
				if error: return res, error
				value, error = self.parser.ParseExpression(res)
				if value in allVariableName:
					value = self.symbolTable.GetVariable(value)[1]
				value = str(value)
				if value.startswith("new Dynamic ("):
					value = value[13:]
					if value.endswith(')'):
						value = value[:-1]
				if value.startswith('"'):
					value = value[1:]
				if value.endswith('"'):
					value = value[:-1]
				if error: return error[0], error[1]
				return value, None
			elif tc[0] == "input":
				value = ""
				for i in tc[1:multipleCommandsIndex + 1]: # Get all parameters provided as 1 long string
					value += i + " "
				value = value[:-1]
				if not value.startswith('('): # Check If the expression has parentheses around or not
					return "InvalidSyntax: Parenthesis is needed after a function name", Exceptions.InvalidSyntax # Return error if not exists
				if not value.endswith(')'): # Check If the expression has parentheses around or not
					return "InvalidSyntax: Parenthesis is needed after an Argument input", Exceptions.InvalidSyntax # Return error if not exists
				value = value[1:-1] # Cut parentheses out of the string
				if value.startswith('"'):
					value = value[1:]
				if value.endswith('"'):
					value = value[:-1]
				res = input(value) # Recieve the Input from the User
				return f"\"{res}\"", None # Return the Recieved Input
			elif tc[0] == "if":
				runCode = self.parser.ParseConditions(self.parser.ParseConditions(tc[1:]))

				if runCode:
					# Run the code If the condition is true.
					isInCodeBlock = False
					commands = []
					command = []
					for i in tc:
						if i == "then":
							isInCodeBlock = True
							continue
						if isInCodeBlock:
							if i == "&&":
								commands.append(command)
								command = []
								continue
							if i == "end":
								commands.append(command)
								command = []
							command.append(i)
					for i in commands:
						res, error = self.analyseCommand(i)
						if res != None:
							print(res)

				return None, None
			elif tc[0] == "exit":
				value = ""
				for i in tc[1:multipleCommandsIndex + 1]: # Get all parameters provided as 1 long string
					value += i + " "
				value = value[:-1]
				if not value.startswith('('): # Check If the expression has parentheses around or not
					return "InvalidSyntax: Parenthesis is needed after a function name", Exceptions.InvalidSyntax # Return error if not exists
				if not value.endswith(')'): # Check If the expression has parentheses around or not
					return "InvalidSyntax: Parenthesis is needed after an Argument input", Exceptions.InvalidSyntax # Return error if not exists
				value = value[1:-1]
				valtype = self.parser.ParseTypeFromValue(value)
				if value.startswith('"'):
					value = value[1:]
				if value.endswith('"'):
					value = value[:-1]
				return f"EXITREQUEST {value}", valtype
			elif tc[0] == "#define":
				try:
					if tc[1] == "interpet":
						# Set Interpreter Settings
						if tc[2] == "enableFunction":
							if tc[3] == "true":
								self.symbolTable.enableFunctionFeature = True
								return None, None
							else:
								self.symbolTable.enableFunctionFeature = False
								return None, None
				except IndexError:
					return "InvalidValue: You needed to describe what you will change.", Exceptions.InvalidValue
			elif tc[0] == "throw":
				return self.throwKeyword(tc, multipleCommandsIndex) # Go to the Throw keyword function
			elif tc[0] == "typeof":
				if tc[1].startswith('('):
					tc[1] = tc[1][1:]
				else: return "InvalidSyntax: Parenthesis is needed after a function name", Exceptions.InvalidSyntax
				if tc[multipleCommandsIndex].endswith(')'):
					tc[multipleCommandsIndex] = tc[multipleCommandsIndex][:-1]
				else: return "InvalidSyntax: Parenthesis is needed after an Argument input", Exceptions.InvalidSyntax
				if(tc[1] in allVariableName):
					return self.symbolTable.GetVariableType(tc[1]), None
				res, error = self.parser.ParseExpression(tc[1:multipleCommandsIndex + 1])
				if error: return error[0], error[1]
				if(not tc[1] in allVariableName and tc[1][0] in ascii_letters):
					return f"InvalidValue: {tc[1]} is not a Variable and Is not a String.", Exceptions.InvalidValue
				res = self.parser.ParseTypeFromValue(res)
				if res == Exceptions.InvalidSyntax:
					return f"InvalidSyntax: A String must starts with Quote (\") and End with quote (\")", Exceptions.InvalidSyntax
				return res, None
			elif tc[0] == "del":
				if tc[1] in allVariableName:
					self.symbolTable.DeleteVariable(tc[1])
					return None, None
				elif tc[1] in allFunctionName:
					self.symbolTable.DeleteFunction(tc[1])
					return None, None
				else:
					return "InvalidValue: The Input is not a variable.", Exceptions.InvalidValue
			elif tc[0] == "func":
				if self.symbolTable.enableFunctionFeature:
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
						# Find all arguments declared.
						argumentsEndIndex = 1
						arguments = []
						# isConstantsKeyword = False
						isTypesKeywordFound = False
						for i in tc[2:endIndex]:
							argumentsEndIndex += 1
							if i.endswith(")"):
								break
						if not tc[2] in allFunctionName:
							return f"NotDefinedException: The {tc[2]} function is not defined. You can't override non-existed function.", Exceptions.NotDefinedException
						else:
							self.symbolTable.SetFunction(tc[2], tc[argumentsEndIndex + 1:endIndex], tc[3:argumentsEndIndex - 1])
							return None, None
					# Find all arguments declared.
					argumentsEndIndex = 1
					arguments = []
					# isConstantsKeyword = False
					isTypesKeywordFound = False
					for i in tc[2:endIndex]:
						argumentsEndIndex += 1
						if i.endswith(")"):
							break
					self.symbolTable.SetFunction(tc[1], tc[argumentsEndIndex + 1:endIndex], arguments)
					return None, None
				else:
					return "This feature is disabled. Use \"#define interpet enableFunction true\" to enable this feature.", None
			elif tc[0] == "loopfor":
				try:
					commands = []
					command = []
					for i in tc[2:]:
						if i == "&&":
							commands.append(command)
							command = []
							continue
						if i == "end":
							commands.append(command)
							command = []
							break
						command.append(i)
					vartable, functable, isenablefunction = self.symbolTable.copyvalue()
					scopedVariableTable = SymbolTable()
					scopedVariableTable.importdata(vartable, functable, isenablefunction)
					commandlexer = Lexer(scopedVariableTable)
					del scopedVariableTable
					index = 0
					output = ""
					if tc[1] in allVariableName:
						tc[1] = self.symbolTable.GetVariable(tc[1])[1]
					while index < int(tc[1]):
						scopedVariableTable = SymbolTable()
						scopedVariableTable.importdata(vartable, functable, isenablefunction)
						commandlexer.symbolTable = scopedVariableTable
						del scopedVariableTable
						for i in commands:
							res, error = commandlexer.analyseCommand(i)
							if error: return res, error
							if res != None: print(res)
						index += 1
					return None, None
				except ValueError:
					return "InvalidValue: Count must be an Integer. (Whole number)", Exceptions.InvalidValue
			elif tc[0] == "switch":
				cases = {}
				case = []
				command = []
				isInCaseBlock = False
				isInDefaultBlock = False
				isAfterCaseKeyword = False
				currentCaseKey = None
				for i in tc[2:]:
					if i == "case":
						isAfterCaseKeyword = True
						continue
					if isAfterCaseKeyword:
						outkey = i
						if outkey in allVariableName:
							outkey = self.symbolTable.GetVariable(outkey)[1]
						currentCaseKey = outkey
						isAfterCaseKeyword = False
						isInCaseBlock = True
						continue
					if isInCaseBlock:
						if i == "&&":
							case.append(command)
							command = []
							continue
						if i == "break":
							cases[currentCaseKey] = case
							case = []
							isInCaseBlock = False
							continue
						command.append(i)
					if i == "end":
						break

				print(cases)

				if tc[1] in allVariableName:
					tc[1] = self.symbolTable.GetVariable(tc[1])[1]

				scopedVariableTable = SymbolTable()
				vartable, functable, isenablefunction = self.symbolTable.copyvalue()
				scopedVariableTable.importdata(vartable, functable, isenablefunction)
				commandLexer = Lexer(scopedVariableTable)

				res, error = (None, None)

				try:
					res, error = commandLexer.analyseCommand(cases[tc[1]])
				except KeyError:
					try:
						res, error = commandLexer.analyseCommand(cases["default"])
					except KeyError:
						pass
				
				return res, error
			else:
				return "NotImplementedException: This feature is not implemented", Exceptions.NotImplementedException
		elif tc[0] in allFunctionName:
			customSymbolTable = self.symbolTable
			functionObject = self.symbolTable.GetFunction(tc[0])
			flex = Lexer(customSymbolTable, self.executor, self.parser)
			res, error = flex.analyseCommand(functionObject[1])
			return res, error
		elif tc[0] == "//":
			return None, None
		else:
			res, error = self.parser.ParseExpression(tc[0:multipleCommandsIndex + 1])
			if(error): return error[0], error[1]
			return res, None