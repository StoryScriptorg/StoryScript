from filehelper import FileHelper
from langParser import Parser
from executor import Executor
from langEnums import *
from string import ascii_letters
from random import randint

# This class is used to store variables and function
class SymbolTable:
	def __init__(self):
		self.variableTable = {"true":(Types.Boolean, 1), "false":(Types.Boolean, 0)}
		self.functionTable = {}
		self.enableFunctionFeature = False
		self.ignoreInfo = False

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

	def SetVariable(self, key, value, vartype, isHeapAllocated):
		self.variableTable[key] = (vartype, value, isHeapAllocated)

	def SetFunction(self, key, value, arguments):
		self.functionTable[key] = (arguments, value)

	def DeleteVariable(self, key):
		del self.variableTable[key]

	def DeleteFunction(self, key):
		del self.functionTable[key]

class Lexer:
	def __init__(self, symbolTable, outFileName, executor=None, parser=None, fileHelper=None):
		self.executor = executor
		self.symbolTable = symbolTable
		self.parser = parser
		self.executor = executor
		self.fileHelper = fileHelper

		if executor == None:
			self.executor = Executor(self.symbolTable)

		if parser == None:
			self.parser = Parser(self.executor)

		if fileHelper == None:
			self.fileHelper = FileHelper(outFileName)
			self.fileHelper.insertHeader("#include <stdio.h>")
			self.fileHelper.insertHeader("#include <stdlib.h>")
			self.fileHelper.insertHeader("")
			self.fileHelper.insertHeader("int main() {")
			self.fileHelper.insertFooter("\treturn 0;")
			self.fileHelper.insertFooter("}")
			self.fileHelper.indentLevel = 1

	def throwKeyword(self, command):
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

	def raiseTranspileError(self, text):
		print("TRANSPILATION ERROR:")
		print(text)
		raise SystemExit

	def analyseCommand(self, tc, varcontext=None):
		isMultipleCommands = False
		multipleCommandsIndex = -1
		# All Keywords
		basekeywords = ["if", "else", "var", "int",
						"bool", "float", "list", "dictionary",
						"tuple", "const", "override", "func",
						"end", "print", "input", "throw",
						"string", "typeof", "del", "namespace",
						"#define", "loopfor", "switch",
						"input", "exit"]

		for i in tc:
			multipleCommandsIndex += 1
			if i == "&&":
				isMultipleCommands = True
				break

		allVariableName = self.symbolTable.GetAllVariableName()
		allFunctionName = self.symbolTable.GetAllFunctionName()

		try:
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
				if tc[0] in ["var", "int", "bool", "float", "list", "dictionary", "tuple", "const", "string"]:
					try:
						tc[3]
						definedType = self.parser.ParseTypeString(tc[0])
						if(tc[1] in self.symbolTable.GetAllVariableName()):
							return f"AlreadyDefined: a Variable {tc[1]} is already defined", Exceptions.AlreadyDefined
						
						# Checking for variable naming violation
						if not (self.parser.CheckNamingViolation(tc[1])):
							return "InvalidValue: a Variable name cannot start with digits.", Exceptions.InvalidValue

						# var(0) a(1) =(2) 3(3)
						# double(0) heap(1) b(2) =(3) 5(4)
						isHeap = False
						if tc[1] == "heap":
							isHeap = True
							res, error = self.analyseCommand(tc[4:multipleCommandsIndex + 1])
							if isinstance(error, Exceptions):
								self.raiseTranspileError(res)
						else:
							res, error = self.analyseCommand(tc[3:multipleCommandsIndex + 1])
							if isinstance(error, Exceptions):
								self.raiseTranspileError(res)
						value = ""

						for i in tc[3:multipleCommandsIndex + 1]:
							value += i + " "
						value = value[:-1]
						vartype = self.parser.ParseTypeFromValue(res)
						if tc[0] != "var":
							# Check If existing variable type matches the New value type
							if definedType != vartype:
								self.raiseTranspileError("InvalidValue: Variable types doesn't match value type.")
						if vartype == Exceptions.InvalidSyntax:
							self.raiseTranspileError("InvalidSyntax: Invalid value")
						res = self.parser.ParseEscapeCharacter(res)
						self.symbolTable.SetVariable(tc[1], res, vartype, isHeap)
						if tc[1] == "heap":
							outvartype = tc[0]
							if tc[0] == "var":
								outvartype = self.parser.ConvertTypesEnumToString(vartype)
							self.fileHelper.insertContent(f"{outvartype} *{tc[2]} = ({outvartype}*)malloc(sizeof({outvartype}));")
							return f"*{tc[2]} = {res};", ""
						if tc[0] == "var":
							outvartype = self.parser.ConvertTypesEnumToString(vartype)
							return f"{outvartype} {tc[1]} = {res};", ""
						return f"{tc[0]} {tc[1]} = {res};", ""
					except IndexError:
						# var(0) a(1)			(Stack allocation)
						# int(0) heap(1) a(2)	(Heap allocation)
						if tc[0] == "var":
							self.raiseTranspileError("InvalidSyntax: Initial value needed for var keyword")
						vartype = self.parser.ParseTypeString(tc[0])
						if vartype == Exceptions.InvalidSyntax:
							self.raiseTranspileError("InvalidSyntax: Invalid type")
						if tc[1] == "heap":
							return f"{tc[0]} *{tc[2]} = ({tc[0]}*)malloc(sizeof({tc[0]}));", ""
						return f"{tc[0]} {tc[1]};", ""
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
					# res, error = self.analyseCommand(svalue)
					# if error: return res, error
					# value, error = self.parser.ParseExpression(res)
					# if value in allVariableName:
					# 	value = self.symbolTable.GetVariable(value)[1]
					value = str(value)
					if value.startswith("new Dynamic ("):
						value = value[13:]
						if value.endswith(')'):
							value = value[:-1]
					# if error: return error[0], error[1]
					return f"printf({value});", None
				elif tc[0] == "input":
					value = ""
					for i in tc[2:multipleCommandsIndex + 1]: # Get all parameters provided as 1 long string
						value += i + " "
					value = value[:-1]
					if not value.startswith('('): # Check If the expression has parentheses around or not
						self.raiseTranspileError("InvalidSyntax: Parenthesis is needed after a function name") # Return error if not exists
					if not value.endswith(')'): # Check If the expression has parentheses around or not
						self.raiseTranspileError("InvalidSyntax: Parenthesis is needed after an Argument input") # Return error if not exists
					value = value[1:-1] # Cut parentheses out of the string
					# if value.startswith('"'):
					# 	value = value[1:]
					# if value.endswith('"'):
					# 	value = value[:-1]
					# res = input(value) # Recieve the Input from the User
					return f"scanf(\"%s\", &{varcontext})", {int(tc[1])} # Return the Recieved Input
				elif tc[0] == "if":
					conditionslist:list = self.parser.ParseConditions(tc[1:])
					allexprResult = []
					for i in conditionslist:
						exprResult = []
						currentConditionType = ConditionType.Single
						for j in i:
							if j and isinstance(j, list):
								exprResult.append(self.parser.ParseConditionExpression(j, lambda tc:self.analyseCommand(tc)))
							elif isinstance(j, ConditionType):
								currentConditionType = j
						if currentConditionType == ConditionType.And:
							res = False
							for i in exprResult:
								if i == True: res = True
								else: res = False
							allexprResult.append(res)
						elif currentConditionType == ConditionType.Single:
							allexprResult.append(exprResult[0])
						elif currentConditionType == ConditionType.Or:
							for i in exprResult:
								if i == True:
									allexprResult.append(True)
									break

					runCode = False
					for i in allexprResult:
						runCode = i

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
						self.raiseTranspileError("InvalidSyntax: Parenthesis is needed after a function name") # Return error if not exists
					if not value.endswith(')'): # Check If the expression has parentheses around or not
						self.raiseTranspileError("InvalidSyntax: Parenthesis is needed after an Argument input") # Return error if not exists
					value = value[1:-1]
					valtype = self.parser.ParseTypeFromValue(value)
					if value.startswith('"'):
						self.raiseTranspileError("InvalidValue: Exit code can only be integer.")
					if value.endswith('"'):
						self.raiseTranspileError("InvalidValue: Exit code can only be integer.")
					if not value:
						self.raiseTranspileError("InvalidValue: Parameter \"status\" (int) required")
					return f"exit({int(value)});", valtype
				elif tc[0] == "#define":
					try:
						if tc[1] == "interpet":
							# Set Interpreter Settings
							if tc[2] == "enableFunction":
								if tc[3] == "true":
									self.symbolTable.enableFunctionFeature = True
									return "", ""
								else:
									self.symbolTable.enableFunctionFeature = False
									return "", ""
							elif tc[2] == "ignoreInfo":
								if tc[3] == "true":
									self.symbolTable.ignoreInfo = True
									return "", ""
								else:
									self.symbolTable.ignoreInfo = False
									return "", ""
					except IndexError:
						self.raiseTranspileError("InvalidValue: You needed to describe what you will change.")
				elif tc[0] == "throw":
					return self.throwKeyword(tc) # Go to the Throw keyword function
				elif tc[0] == "del":
					if not self.symbolTable.ignoreInfo:
						print("INFO: del keyword only works on Heap allocated variable. Stack allocated variable will only get Deleted on Out of Scope.")
					return f"free({tc[1]})", ""
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
						commands = [] # list of commands
						command = []
						endkeywordcount = 0 # All "end" keyword in the expression
						endkeywordpassed = 0 # All "end" keyword passed
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
						genvarname = None
						genvarname = "__sts_loopcount_"
						genvarname += ascii_letters[randint(0, 51)]
						genvarname += ascii_letters[randint(0, 51)]
						genvarname += ascii_letters[randint(0, 51)]
						self.fileHelper.insertContent(f"for (int {genvarname} = 0; {genvarname} < {int(tc[1])}; {genvarname}++)" + " {")
						self.fileHelper.indentLevel += 1
						for i in commands:
							self.fileHelper.insertContent(self.analyseCommand(i)[0])
						self.fileHelper.indentLevel -= 1
						self.fileHelper.insertContent("}")
						return "", ""
					except ValueError:
						self.raiseTranspileError("InvalidValue: Count must be an Integer. (Whole number)")
				elif tc[0] == "switch":
					cases = []
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
								cases.append((currentCaseKey, case))
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
					commandLexer = Lexer(scopedVariableTable, self.fileHelper.filename)

					defaultCase = False
					
					self.fileHelper.insertContent(f"switch ({tc[1]})")
					self.fileHelper.insertContent("{")
					self.fileHelper.indentLevel += 1
					for i in cases:
						if i[0] == "default":
							defaultCase = i
							continue
						self.fileHelper.insertContent(f"case {i[0]}:")
						self.fileHelper.indentLevel += 1
						for j in i[1]:
							self.fileHelper.insertContent(self.analyseCommand(j))
						self.fileHelper.insertContent("break;")
						self.fileHelper.indentLevel -= 1
					if defaultCase:
						self.fileHelper.insertContent("default:")
						self.fileHelper.indentLevel += 1
						for j in i[1]:
							self.fileHelper.insertContent(self.analyseCommand(j))
						self.fileHelper.insertContent("break;")
						self.fileHelper.indentLevel -= 1
					self.fileHelper.indentLevel -= 1
					self.fileHelper.insertContent("}")

					return "", ""
				else:
					self.raiseTranspileError("NotImplementedException: This feature is not implemented")
			elif tc[0] in allFunctionName:
				customSymbolTable = self.symbolTable
				functionObject = self.symbolTable.GetFunction(tc[0])
				flex = Lexer(customSymbolTable, self.executor, self.parser)
				res, error = flex.analyseCommand(functionObject[1])
				return res, error
			elif tc[0] == "//":
				res = ""
				for i in tc:
					res += i + " "
				return res, ""
			else:
				res, error = self.parser.ParseExpression(tc[0:multipleCommandsIndex + 1])
				if(error): return error[0], error[1]
				return res, None
		except IndexError:
			return "", ""