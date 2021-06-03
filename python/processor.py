from langEnums import *
from sys import argv
from lexer import Lexer

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

GlobalVariableTable = SymbolTable()

def execute(command):
	trimmedCommand = command.split()

	lexer = Lexer(GlobalVariableTable)
	res, error = lexer.analyseCommand(trimmedCommand)

	return res

STORYSCRIPT_INTERPRETER_DEBUG_MODE = True

def parseFile(fileName):
	if STORYSCRIPT_INTERPRETER_DEBUG_MODE:
		import os
		print("[DEBUG] Current Working Directory: " + os.getcwd())
	try:
		f = open(fileName, "r")
	except FileNotFoundError:
		print(f"Cannot open file {fileName}. File does not exist.")
		return
	lexer = Lexer(GlobalVariableTable)
	lines = f.readlines()
	for i in lines:
		i = i.split()
	command = []
	isMultilineEnd = False
	for i in lines:
		commands = i.split()
		if "loopfor" in commands or "switch" in commands:
			isMultilineEnd = True
			command += commands
			continue
		if "end" in commands:
			isMultilineEnd = False
		res, error = lexer.analyseCommand(commands)
		if res != None:
			print(res)

if __name__ == "__main__":
	parseFile(argv[1])