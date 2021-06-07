from langEnums import *
from sys import argv
from lexer import Lexer, SymbolTable
from langEnums import *

GlobalVariableTable = SymbolTable()
STORYSCRIPT_INTERPRETER_DEBUG_MODE = True

def ParseStringList(self, command):
		res = ""
		for i in command:
			res += i + " "
		res = res[:-1]
		return res

def parseFile(outFile, fileName):
	if STORYSCRIPT_INTERPRETER_DEBUG_MODE:
		import os
		print("[DEBUG] Current Working Directory: " + os.getcwd())
	try:
		f = open(fileName, "r")
	except FileNotFoundError:
		print(f"Cannot open file {fileName}. File does not exist.")
		return
	lexer = Lexer(GlobalVariableTable, outFile)
	lines = f.readlines()
	isInMultilineInstructions = False
	for i in lines:
		commands = i.split()
		lexer.fileHelper.insertContent(lexer.analyseCommand(commands)[0])
	lexer.fileHelper.writeDataToFile()

if __name__ == "__main__":
	# python processor.py
	isInNamedArguments = False
	outputFile = ""
	inputFile = ""
	for i in argv:
		if i == "-o" or i == "--output":
			isInNamedArguments = "-o"
			continue
		elif i == "-i" or i == "--input":
			isInNamedArguments = "-i"
			continue
		if isInNamedArguments:
			if isInNamedArguments == "-o":
				outputFile = i
			elif isInNamedArguments == "-i":
				inputFile = i
			isInNamedArguments = False
	parseFile(outputFile, inputFile)