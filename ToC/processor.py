from langEnums import *
from sys import argv
from lexer import Lexer, SymbolTable, libraryIncluded
from langEnums import *
from tqdm import tqdm
from time import perf_counter
import tracemalloc

GlobalVariableTable = SymbolTable()
STORYSCRIPT_INTERPRETER_DEBUG_MODE = True

def ParseStringList(self, command):
		res = ""
		for i in command:
			res += i + " "
		res = res[:-1]
		return res

def parseFile(outFile, fileName, autoReallocate=True):
	tracemalloc.start()
	start_time = perf_counter()
	if STORYSCRIPT_INTERPRETER_DEBUG_MODE:
		import os
		print("[DEBUG] Current Working Directory: " + os.getcwd())
	try:
		f = open(fileName, "r")
	except FileNotFoundError:
		print(f"Cannot open file {fileName}. File does not exist.")
		return
	if not autoReallocate:
		print("[DEBUG] Auto reallocate turned off. Please note that Buffer over flow is not warned.")
	lexer = Lexer(GlobalVariableTable, outFile, autoReallocate=autoReallocate)
	lines = f.readlines()
	lineIndex = 0
	isInMultilineInstructions = False
	print("Conversion starting...")
	for i in tqdm(lines, ncols=50):
		lineIndex += 1
		commands = i.split()
		lexer.fileHelper.insertContent(lexer.analyseCommand(commands, ln=lineIndex)[0])
	print("Conversion done. Writing data to file...")
	for i in libraryIncluded:
		lexer.fileHelper.insertHeader(f"#include <{i}>")
	lexer.fileHelper.insertHeader('''
// Exception Raising
void raiseException(int code, char* description)
{
	switch(code)
	{
		case 100:
			printf("InvalidSyntax: %s", description);
			break;
		case 101:
			printf("AlreadyDefined: %s", description);
			break;
		case 102:
			printf("NotImplementedException %s", description);
			break;
		case 103:
			printf("NotDefinedException: %s", description);
			break;
		case 104:
			printf("GeneralException: %s", description);
			break;
		case 105:
			printf("DivideByZeroException: %s", description);
			break;
		case 106:
			printf("InvalidValue: %s", description);
			break;
		case 107:
			printf("InvalidTypeException: %s", description);
			break;
	}
	exit(code);
}
''')
	lexer.fileHelper.insertHeader("int main() {")
	lexer.fileHelper.writeDataToFile()
	print("Successfully written data to file.")
	print(" -- Statistics -- ")
	current, peak = tracemalloc.get_traced_memory()
	finish_time = perf_counter()
	print(f'Memory usage:\t\t {current / 10**6:.6f} MB \n'
		  f'Peak memory usage:\t {peak / 10**6:.6f} MB ')
	print(f'Time elapsed in seconds: {finish_time - start_time:.6f}')
	print(f'{"-"*40}')
	tracemalloc.stop()

if __name__ == "__main__":
	# python processor.py -o main.c -i main.sts
	print("// StoryScript C Transpiler // Version Alpha 1 //")
	isInNamedArguments = False
	outputFile = ""
	inputFile = ""
	autoReallocate = True
	for i in argv:
		if i == "-o" or i == "--output":
			isInNamedArguments = "-o"
			continue
		elif i == "-i" or i == "--input":
			isInNamedArguments = "-i"
			continue
		elif i == "--no-auto-reallocate" or i == "-no-realloc":
			autoReallocate = False
		if isInNamedArguments:
			if isInNamedArguments == "-o":
				outputFile = i
			elif isInNamedArguments == "-i":
				inputFile = i
			isInNamedArguments = False
	parseFile(outputFile, inputFile, autoReallocate)