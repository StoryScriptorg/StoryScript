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

	def SetVariable(self, key, value, vartype, isHeapAllocated=False, strSize=None):
		self.variableTable[key] = (vartype, value, isHeapAllocated, strSize)

	def SetFunction(self, key, value, arguments):
		self.functionTable[key] = (arguments, value)

	def DeleteVariable(self, key):
		del self.variableTable[key]

	def DeleteFunction(self, key):
		del self.functionTable[key]

global libraryIncluded
libraryIncluded:list = ["stdio.h", "stdlib.h"]

class Lexer:
	def __init__(self, symbolTable, outFileName, executor=None, parser=None, fileHelper=None, autoReallocate=True):
		self.executor = executor
		self.symbolTable = symbolTable
		self.parser = parser
		self.executor = executor
		self.fileHelper = fileHelper
		self.autoReallocate = autoReallocate

		if executor == None:
			self.executor = Executor(self.symbolTable)

		if parser == None:
			self.parser = Parser(self.executor)

		if fileHelper == None:
			self.fileHelper = FileHelper(outFileName)
			self.fileHelper.insertFooter("\treturn 0;")
			self.fileHelper.insertFooter("}")
			self.fileHelper.indentLevel = 1

	def throwKeyword(self, tc, multipleCommandsIndex, ln="Unknown"):
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
					return f"raiseException(100, \"{msg}\");", ""
				else: raise IndexError
			except IndexError:
				return "raiseException(100, \"No Description provided\");", Exceptions.InvalidSyntax
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
					return f"raiseException(101, \"{msg}\");", Exceptions.AlreadyDefined
				else: raise IndexError
			except IndexError:
				return "raiseException(101, \"No Description provided\");", Exceptions.AlreadyDefined
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
					return f"raiseException(102, \"{msg}\");", Exceptions.NotImplementedException
				else: raise IndexError
			except IndexError:
				return "raiseException(102, \"This feature is not implemented\");", Exceptions.NotImplementedException
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
					return f"raiseException(103, \"{msg}\");", Exceptions.NotDefinedException
				else: raise IndexError
			except IndexError:
				return "raiseException(103, \"No Description provided\");", Exceptions.NotDefinedException
		elif(tc[1] == "GeneralException"):
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
					return f"raiseException(104, \"{msg}\");", Exceptions.GeneralException
				else: raise IndexError
			except IndexError:
				return "raiseException(104, \"No Description provided\");", Exceptions.GeneralException
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
					return f"raiseException(105, \"{msg}\");", Exceptions.DivideByZeroException
				else: raise IndexError
			except IndexError:
				return "raiseException(105, \"You cannot divide numbers with 0\");", Exceptions.DivideByZeroException
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
					return f"raiseException(106, \"{msg}\");", Exceptions.InvalidValue
				else: raise IndexError
			except IndexError:
				return "raiseException(106, \"No Description provided\");", Exceptions.InvalidValue
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
					return f"raiseException(107, \"{msg}\");", Exceptions.InvalidTypeException
				else: raise IndexError
			except IndexError:
				return "raiseException(107, \"No Description provided\");", Exceptions.InvalidTypeException
		else:
			self.raiseTranspileError("InvalidValue: The Exception entered is not defined", ln)

	def raiseTranspileError(self, text, ln="Unknown"):
		print("TRANSPILATION ERROR:")
		print(f"While processing line {ln}")
		print(text)
		raise SystemExit

	def analyseCommand(self, tc, ln="Unknown", varcontext=None):
		isMultipleCommands = False
		multipleCommandsIndex = -1
		# All Keywords
		basekeywords = ["if", "else", "var", "int",
						"bool", "float", "list", "dictionary",
						"tuple", "const", "override", "func",
						"end", "print", "input", "throw",
						"string", "del", "namespace",
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
						oldvar = self.symbolTable.GetVariable(tc[0])
						if error: self.raiseTranspileError(error[0], ln)
						if oldvar[2]:
							if oldvar[0] == Types.String:
								error = self.symbolTable.SetVariable(tc[0], res, vartype, oldvar[2], len(res) - 1)
								if self.autoReallocate:
									if oldvar[3] < (len(res) - 1):
										self.fileHelper.insertContent(f"{tc[0]} = realloc({tc[0]}, {len(res) - 1});")
									else:
										if oldvar[3] > len(res) - 1 and oldvar[3] > 64:
											self.fileHelper.insertContent(f"{tc[0]} = realloc({tc[0]}, {len(res) - 1});")
								else:
									print("INFO: To set a Message to a String, Input string must be less than the Size specified or equal the Original string size If declared with initial value.")
									if lenght > oldvar[3]:
										self.raiseTranspileError("InvalidValue: The input string length is more than the Original Defined size. If you want a Dynamically allocated string, Please don't use \"--no-auto-reallocate\" option.", ln)
								return f"memcpy({tc[0]}, {res}, {len(res) - 1});", ""
							return f"*{tc[0]} = {res};", ""
						if vartype == Types.String:
							length = len(res) - 1
							error = self.symbolTable.SetVariable(tc[0], res, vartype, oldvar[2], length)
							if length > oldvar[3]:
								self.raiseTranspileError("InvalidValue: The input string length is more than the Original Defined size. If you want a Dynamically allocated string, Please use the Heap allocated string instead If you want to make the String dynamiccally allocated.", ln)
							return f"memcpy({tc[0]}, {res}, {length});", ""
						error = self.symbolTable.SetVariable(tc[0], res, vartype, oldvar[2])
						return f"{tc[0]} = {res};", ""
					elif tc[1] == "+=": # Add & Set operator
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
						oldvar = self.symbolTable.GetVariable(tc[0])
						error = self.symbolTable.SetVariable(tc[0], res, vartype, oldvar[2])
						if error: self.raiseTranspileError(error[0], ln)
						if oldvar[2]:
							if oldvar[0] == Types.String:
								self.raiseTranspileError("InvalidTypeException: You cannot use += with String.", ln)
							return f"*{tc[0]} += {res};", ""
						return f"{tc[0]} += {res};", ""
					elif tc[1] == "-=": # Subtract & Set operator
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
						oldvar = self.symbolTable.GetVariable(tc[0])
						error = self.symbolTable.SetVariable(tc[0], res, vartype, oldvar[2])
						if error: self.raiseTranspileError(error[0], ln)
						if oldvar[2]:
							if oldvar[0] == Types.String:
								self.raiseTranspileError("InvalidTypeException: You cannot use -= with String.", ln)
							return f"*{tc[0]} -= {res};", ""
						return f"{tc[0]} -= {res};", ""
					elif tc[1] == "*=": # Multiply & Set operator
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
						oldvar = self.symbolTable.GetVariable(tc[0])
						error = self.symbolTable.SetVariable(tc[0], res, vartype, oldvar[2])
						if error: self.raiseTranspileError(error[0], ln)
						if oldvar[2]:
							if oldvar[0] == Types.String:
								self.raiseTranspileError("InvalidTypeException: You cannot use *= with String.", ln)
							return f"*{tc[0]} *= {res};", ""
						return f"{tc[0]} *= {res};", ""
					elif tc[1] == "/=": # Divide & Set operator
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
						oldvar = self.symbolTable.GetVariable(tc[0])
						error = self.symbolTable.SetVariable(tc[0], res, vartype, oldvar[2])
						if error: self.raiseTranspileError(error[0], ln)
						if oldvar[2]:
							if oldvar[0] == Types.String:
								self.raiseTranspileError("InvalidTypeException: You cannot use /= with String.", ln)
							return f"*{tc[0]} /= {res};", ""
						return f"{tc[0]} /= {res};", ""
					elif tc[1] == "%=": # Modulo Operaion & Set operator
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
						oldvar = self.symbolTable.GetVariable(tc[0])
						error = self.symbolTable.SetVariable(tc[0], res, vartype, oldvar[2])
						if error: self.raiseTranspileError(error[0], ln)
						if oldvar[2]:
							if oldvar[0] == Types.String:
								self.raiseTranspileError("InvalidTypeException: You cannot use %= with String.", ln)
							return f"*{tc[0]} %= {res};", ""
						return f"{tc[0]} %= {res};", ""
					else:
						res = ""
						for i in tc:
							res += i + " "
						res = res[:-1]
						return res, ""
				except IndexError:
					res = ""
					for i in tc:
						res += i + " "
					res = res[:-1]
					return res, ""
			elif tc[0] in basekeywords:
				if tc[0] in ["var", "int", "bool", "float", "list", "dictionary", "tuple", "const", "string"]:
					try:
						if tc[2] == "=" or tc[3] == "=": pass
						else: raise IndexError
						definedType = self.parser.ParseTypeString(tc[0])
						if(tc[1] in self.symbolTable.GetAllVariableName()):
							self.raiseTranspileError(f"AlreadyDefined: a Variable \"{tc[1]}\" is already defined", ln)
						
						# Checking for variable naming violation
						if not (self.parser.CheckNamingViolation(tc[1])):
							self.raiseTranspileError("InvalidValue: a Variable name cannot start with digits.", ln)

						# var(0) a(1) =(2) 3(3)
						# double(0) heap(1) b(2) =(3) 5(4)
						isHeap = False
						if tc[1] == "heap":
							isHeap = True
							res, error = self.analyseCommand(tc[4:multipleCommandsIndex + 1], tc[2])
							if isinstance(error, Exceptions):
								self.raiseTranspileError(res, ln)
						else:
							res, error = self.analyseCommand(tc[3:multipleCommandsIndex + 1], tc[1])
							if isinstance(error, Exceptions):
								self.raiseTranspileError(res, ln)
						value = ""

						for i in tc[3:multipleCommandsIndex + 1]:
							value += i + " "
						value = value[:-1]
						vartype = self.parser.ParseTypeFromValue(res)
						if tc[0] != "var":
							# Check If existing variable type matches the New value type
							if definedType != vartype:
								self.raiseTranspileError("InvalidValue: Variable types doesn't match value type.", ln)
						if vartype == Exceptions.InvalidSyntax:
							self.raiseTranspileError("InvalidSyntax: Invalid value", ln)
						res = self.parser.ParseEscapeCharacter(res)

						if isHeap:
							outvartype = tc[0]
							if tc[0] == "var":
								outvartype = self.parser.ConvertTypesEnumToString(vartype)
							if vartype == Types.String:
								if "string.h" not in libraryIncluded:
									libraryIncluded.append("string.h")
								self.symbolTable.SetVariable(tc[2], res, vartype, True, len(res) - 1)
								self.fileHelper.insertContent(f"char *{tc[2]} = (char*)malloc({len(res) - 1});")
								return f"if({tc[2]} != NULL) memcpy({tc[2]}, {res}, {len(res) - 1});", ""
							self.symbolTable.SetVariable(tc[2], res, vartype, True)
							self.fileHelper.insertContent(f"{outvartype} *{tc[2]} = ({outvartype}*)malloc(sizeof({outvartype}));")
							return f"*{tc[2]} = {res};", ""
						if tc[0] == "var":
							outvartype = self.parser.ConvertTypesEnumToString(vartype)
							if vartype == Types.String:
								self.symbolTable.SetVariable(tc[1], res, vartype, False, len(res) - 1)
								return f"char {tc[1]}[{len(res) - 1}] = {res};", ""
							self.symbolTable.SetVariable(tc[1], res, vartype, False)
							return f"{outvartype} {tc[1]} = {res};", ""
						if vartype == Types.String:
								self.symbolTable.SetVariable(tc[1], res, vartype, False, len(res) - 1)
								return f"char {tc[1]}[{len(res) - 1}] = {res};", ""
						self.symbolTable.SetVariable(tc[1], res, vartype, isHeap)
						return f"{tc[0]} {tc[1]} = {res};", ""
					except IndexError:
						# var(0) a(1)			(Stack allocation)
						# int(0) heap(1) a(2)	(Heap allocation)
						# string(0) heap(1) a(2) 20(3) (String heap allocation)
						if tc[0] == "var":
							print("[DEBUG]: Command:", tc)
							self.raiseTranspileError("InvalidSyntax: Initial value needed for var keyword", ln)
						vartype = self.parser.ParseTypeString(tc[0])
						if vartype == Exceptions.InvalidSyntax:
							self.raiseTranspileError("InvalidSyntax: Invalid type", ln)
						if tc[1] == "heap":
							if vartype == Types.String:
								self.symbolTable.SetVariable(tc[2], None, vartype, True, int(tc[3]))
								if "string.h" not in libraryIncluded:
									libraryIncluded.append("string.h")
								return f"char *{tc[2]} = (char*)malloc({tc[3]});", ""
							self.symbolTable.SetVariable(tc[2], None, vartype, True)
							return f"{tc[0]} *{tc[2]} = ({tc[0]}*)malloc(sizeof({tc[0]}));", ""
						self.symbolTable.SetVariable(tc[1], None, vartype, False)
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
					value = str(value)
					return f"printf({value});", None
				elif tc[0] == "input":
					value = ""
					for i in tc[2:multipleCommandsIndex + 1]: # Get all parameters provided as 1 long string
						value += i + " "
					value = value[:-1]
					if not value.startswith('('): # Check If the expression has parentheses around or not
						self.raiseTranspileError("InvalidSyntax: Parenthesis is needed after a function name", ln) # Return error if not exists
					if not value.endswith(')'): # Check If the expression has parentheses around or not
						self.raiseTranspileError("InvalidSyntax: Parenthesis is needed after an Argument input", ln) # Return error if not exists
					value = value[1:-1] # Cut parentheses out of the string
					# if value.startswith('"'):
					# 	value = value[1:]
					# if value.endswith('"'):
					# 	value = value[:-1]
					# res = input(value) # Recieve the Input from the User
					return f"scanf(\"%s\", &{varcontext})", {int(tc[1])} # Return the Recieved Input
				elif tc[0] == "if":
					conditionslist:list = self.parser.ParseConditions(tc[1:])
					finalString = "if ("
					for i in conditionslist:
						exprs = []
						currentConditionType = ConditionType.Single
						for j in i:
							if j and isinstance(j, list):
								exprs.append(j)
							elif isinstance(j, ConditionType):
								currentConditionType = j
						if currentConditionType == ConditionType.And:
							for i in exprs:
								finalString += self.parser.ParseStringList(i) + " && "
							finalString = finalString[:-4]
						elif currentConditionType == ConditionType.Single:
							finalString += self.parser.ParseStringList(exprs[0])
						elif currentConditionType == ConditionType.Or:
							for i in exprs:
								finalString += self.parser.ParseStringList(i) + "||"
							finalString = finalString[:-4]
					finalString += ")"

					isInCodeBlock = False
					isInElseBlock = False
					havePassedThenKeyword = False
					ifstatement = {"if":[], "else":None}
					commands = []
					command = []
					endkeywordcount = 0 # All "end" keyword in the expression
					endkeywordpassed = 0 # All "end" keyword passed
					for i in tc[2:]:
						if i == "end":
							endkeywordcount += 1
					for i in tc:
						if not havePassedThenKeyword:
							if i == "then":
								isInCodeBlock = True
								havePassedThenKeyword = True
								continue
						if isInCodeBlock:
							if i == "&&":
								commands.append(command)
								command = []
								continue
							elif i == "end":
								endkeywordpassed += 1
								if endkeywordcount == endkeywordpassed:
									commands.append(command)
									command = []
									if isInElseBlock:
										ifstatement["else"] = commands
									else: ifstatement["if"] = commands
									isInElseBlock = False
									isInCodeBlock = False
							elif i == "else":
								commands.append(command)
								command = []
								ifstatement["if"] = commands
								commands = []
								isInElseBlock = True
							command.append(i)
					print(endkeywordcount, endkeywordpassed)
					print(commands)
					self.fileHelper.insertContent(finalString)
					self.fileHelper.insertContent("{")
					self.fileHelper.indentLevel +=  1
					for i in ifstatement["if"]:
						self.fileHelper.insertContent(self.analyseCommand(i)[0])
					self.fileHelper.indentLevel -= 1
					if ifstatement["else"] != None:
						self.fileHelper.insertContent("} else {")
						self.fileHelper.indentLevel +=  1
						for i in ifstatement["else"]:
							self.fileHelper.insertContent(self.analyseCommand(i)[0])
						self.fileHelper.indentLevel -= 1
						self.fileHelper.insertContent("}")
					else: self.fileHelper.insertContent("}")

					return "", ""
				elif tc[0] == "exit":
					value = ""
					for i in tc[1:multipleCommandsIndex + 1]: # Get all parameters provided as 1 long string
						value += i + " "
					value = value[:-1]
					if not value.startswith('('): # Check If the expression has parentheses around or not
						self.raiseTranspileError("InvalidSyntax: Parenthesis is needed after a function name", ln) # Return error if not exists
					if not value.endswith(')'): # Check If the expression has parentheses around or not
						self.raiseTranspileError("InvalidSyntax: Parenthesis is needed after an Argument input", ln) # Return error if not exists
					value = value[1:-1]
					valtype = self.parser.ParseTypeFromValue(value)
					if value.startswith('"'):
						self.raiseTranspileError("InvalidValue: Exit code can only be integer.", ln)
					if value.endswith('"'):
						self.raiseTranspileError("InvalidValue: Exit code can only be integer.", ln)
					if not value:
						self.raiseTranspileError("InvalidValue: Parameter \"status\" (int) required.", ln)
					return f"exit({int(value)});", valtype
				elif tc[0] == "#define":
					try:
						if tc[1] == "interpet":
							# Set Interpreter Settings
							if tc[2] == "enableFunction":
								if tc[3] == "true":
									if not self.symbolTable.ignoreInfo:
										print("[DEBUG] INFO: Enable function")
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
									print("[DEBUG] INFO: Ignore info disabled")
									self.symbolTable.ignoreInfo = False
									return "", ""
					except IndexError:
						self.raiseTranspileError("InvalidValue: You needed to describe what you will change.", ln)
				elif tc[0] == "throw":
					return self.throwKeyword(tc, multipleCommandsIndex) # Go to the Throw keyword function
				elif tc[0] == "del":
					if tc[1] not in allVariableName:
						self.RaiseTranspileError(f"NotDefinedException: The variable {tc[1]} is not defined.", ln)
					if not self.symbolTable.GetVariable(tc[1])[2]:
						self.raiseTranspileError(f"InvalidValue: The variable {tc[1]} is not heap allocated.", ln)
					return f"free({tc[1]});", ""
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
						self.raiseTranspileError("InvalidValue: Count must be an Integer. (Whole number)", ln)
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
								case.append(command)
								cases.append((currentCaseKey, case))
								command = []
								case = []
								isInCaseBlock = False
								continue
							command.append(i)
						if i == "end":
							break

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
							self.fileHelper.insertContent(self.analyseCommand(j)[0])
						self.fileHelper.insertContent("break;")
						self.fileHelper.indentLevel -= 1
					if defaultCase:
						self.fileHelper.insertContent("default:")
						self.fileHelper.indentLevel += 1
						for j in i[1]:
							self.fileHelper.insertContent(self.analyseCommand(j)[0])
						self.fileHelper.insertContent("break;")
						self.fileHelper.indentLevel -= 1
					self.fileHelper.indentLevel -= 1
					self.fileHelper.insertContent("}")

					return "", ""
				else:
					self.raiseTranspileError("NotImplementedException: This feature is not implemented", ln)
			elif tc[0] in allFunctionName:
				res = ""
				for i in tc:
					res += i + " "
				res = res[:-1]
				return res, ""
			elif tc[0] == "//":
				res = ""
				for i in tc:
					res += i + " "
				return res, ""
			else:
				res = ""
				for i in tc:
					res += i + " "
				res = res[:-1]
				return res, ""
		except IndexError:
			return "", ""