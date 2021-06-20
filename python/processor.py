from langEnums import Types
from sys import argv
from lexer import Lexer, SymbolTable
from sys import exit as sysexit

GlobalVariableTable = SymbolTable()

def execute(command):
    trimmedCommand = command.split()

    lexer = Lexer(GlobalVariableTable)
    res, error = lexer.analyseCommand(trimmedCommand)

    return res

STORYSCRIPT_INTERPRETER_DEBUG_MODE = True

def parse_string_list(self, command):
        res = ""
        for i in command:
            res += i + " "
        res = res[:-1]
        return res

def parse_file(fileName):
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
        if res is not None:
            if res.startswith("EXITREQUEST"):
                code = res.removeprefix("EXITREQUEST ")
                if error == Types.Integer:
                    code = int(code)
                elif error == Types.Float:
                    code = float(code)
                if STORYSCRIPT_INTERPRETER_DEBUG_MODE:
                    print(f"[DEBUG] Application exited with code: {code}")
                sysexit(code)
            print(res)

if __name__ == "__main__":
    parse_file(argv[1])