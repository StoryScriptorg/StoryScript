from langEnums import *
from sys import argv
from lexer import Lexer, SymbolTable
from langEnums import *

GlobalVariableTable = SymbolTable()

def execute(command):
	trimmedCommand = command.split()

	lexer = Lexer(GlobalVariableTable)
	res, error = lexer.analyseCommand(trimmedCommand)

	return res

STORYSCRIPT_INTERPRETER_DEBUG_MODE = True

def ParseStringList(self, command):
		res = ""
		for i in command:
			res += i + " "
		res = res[:-1]
		return res

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
	isInMultilineInstructions = False
	for i in lines:
		commands = i.split()
		res, error = lexer.analyseCommand(commands)
		if res != None:
			if res.startswith("EXITREQUEST"):
				code = res.removeprefix("EXITREQUEST ")
				if error == Types.Integer:
					code = int(code)
				elif error == Types.Float:
					code = float(code)
				if STORYSCRIPT_INTERPRETER_DEBUG_MODE:
					print(f"[DEBUG] Application exited with code: {code}")
				exit(code)
			print(res)

if __name__ == "__main__":
	parseFile(argv[1])