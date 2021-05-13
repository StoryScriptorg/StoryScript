from enum import Enum

class Exceptions(Enum):
	InvalidSyntax	= 100
	AlreadyDefined	= 101

class Types(Enum):
	Boolean = 0
	Integer = 1
	Float	= 2
	List	= 3
	Dictionary = 4
	Tuple	= 5

# Trim & Split to make commands understandable by Lexer
class CommandTrimmer:
	def __init__(self):
		pass

	def analyseCommand(self, command):
		if command.endswith("\n"):
			command = command[:-1]
		res = command.split()
		return res

	def analyseCommands(self, commands):
		res = []
		for i in commands:
			if command.endswith("\n"):
				command = command[:-1]
			res.append(command.split())
		return res

# This class is used to store variables and function
class SymbolTable:
	def __init__(self):
		self.variableTable = {"true":(Types.Boolean, 1), "false":(Types.Boolean, 0)}
		self.functionTable = {}

	def GetAllVariableName(self):
		return self.variableTable.keys()

	def GetVariable(self, key):
		return self.variableTable[key]

	def GetFunction(self, key):
		return self.functionTable[key]

	def SetVariable(self, key, value):
		self.variableTable[key] = value

	def SetFunction(self, key, value):
		self.functionTable[key] = value

class Executor:
	def __init__(self, symbolTable):
		pass

	def add(self, command):
		# Adding numbers.
		pass

	def subtract(self, command):
		# Subtract numbers.
		pass

	def multiply(self, command):
		pass

	def divide(self, command):
		pass

	def pow(self, command):
		pass

class Parser:
	def __init__(self):
		pass

	def ParseStringList(self, command):
		res = ""
		for i in command:
			res += i + " "
		res = res[:-1]
		return res

class Lexer:
	def __init__(self, trimmedCommand, symbolTable, executor=None, parser=None):
		self.command = trimmedCommand
		self.executor = executor
		self.symbolTable = symbolTable
		self.parser = parser

		if executor == None:
			self.executor = Executor(self.symbolTable)

		if parser == None:
			self.parser = Parser()

	def analyseCommand(self):
		tc = self.command
		isMultipleCommands = False
		multipleCommandsIndex = -1
		# All Keywords
		basekeywords = ["if", "else", "var", "int",
						"bool", "float", "list", "dictionary",
						"tuple", "const", "override", "func",
						"end", "print", "input"]

		for i in tc:
			multipleCommandsIndex += 1
			if i == "&&":
				isMultipleCommands = True
				break

		if tc[0] in self.symbolTable.GetAllVariableName():
			try:
				if tc[1] == "=":
					if tc[3] == "+":
						res = self.executor.add(tc[2:multipleCommandsIndex])
						if res == Exceptions.InvalidSyntax:
							return "InvalidSyntax: Expected numbers after + sign\nAt keyword 4", Exceptions.InvalidSyntax
						self.symbolTable.SetVariable(tc[0], res)
					else:
						self.symbolTable.SetVariable(tc[0], tc[2:multipleCommandsIndex])
						return None, None
			except IndexError:
				return self.symbolTable.GetVariable(tc[0]), None
		elif tc[0] in basekeywords:
			if tc[0].lower() in ["var", "int", "bool", "float", "list", "dictionary", "tuple", "const"]:
				try:
					if(tc[1] in self.symbolTable.GetAllVariableName()):
						return f"AlreadyDefined: a Variable {tc[1]} is already defined", Exceptions.AlreadyDefined
					# var(0) a(1) =(2) 3(3)
					self.symbolTable.SetVariable(tc[1], tc[3])
					return None, None
				except IndexError:
					# var(0) a(1)
					self.symbolTable.SetVariable(tc[1], None)
					return None, None
			elif tc[0] == "print":
				if not tc[1].startswith("("):
					return "InvalidSyntax: Expected \"(\" before an argument input", Exceptions.InvalidSyntax
				tc[1] = tc[1:]
				if not (tc[multipleCommandsIndex]).endswith(")"):
					return "InvalidSyntax: Expected \")\" after an argument input", Exceptions.InvalidSyntax
				tc[multipleCommandsIndex] = tc[multipleCommandsIndex][:-1]
				if tc[1] in self.symbolTable.GetAllVariableName():
					return self.symbolTable.GetVariable(), None
				string = self.parser.ParseStringList(tc[1:multipleCommandsIndex])
				return string, None

GlobalVariableTable = SymbolTable()

def execute(command):
	trimmedCommand = CommandTrimmer().analyseCommand(command)

	lexer = Lexer(trimmedCommand, GlobalVariableTable)
	res, error = lexer.analyseCommand()

	return res

def parseFile(path):
	pass