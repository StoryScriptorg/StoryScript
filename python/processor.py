from langEnums import Types
from sys import argv
from lexer import Lexer, SymbolTable
import sys

GlobalVariableTable = SymbolTable()

def execute(command):
    trimmedCommand = command.split()

    lexer = Lexer(GlobalVariableTable)
    res = lexer.analyseCommand(trimmedCommand)[0]

    return res

STORYSCRIPT_INTERPRETER_DEBUG_MODE = True

def parse_file(fileName, input_simulate_file, returnOutput=False):
    # Resetting symbol table before running another code
    GlobalVariableTable = SymbolTable()

    stdout = []
    if input_simulate_file:
        sys.stdin = open(input_simulate_file, "r")
    if STORYSCRIPT_INTERPRETER_DEBUG_MODE:
        import os
        print("[DEBUG] Current Working Directory: " + os.getcwd())
    try:
        with open(fileName, "r") as f:
            lexer = Lexer(GlobalVariableTable)
            lines = f.readlines()
            for i in lines:
                commands = i.split()
                res, error = lexer.analyseCommand(commands)
                if res is not None:
                    if res.startswith("EXITREQUEST"):
                        code = res.removeprefix("EXITREQUEST ")
                        try:
                            if error == Types.Integer:
                                code = int(code)
                            elif error == Types.Float:
                                code = float(code)
                        except ValueError:
                            code = 0
                        if STORYSCRIPT_INTERPRETER_DEBUG_MODE:
                            print(f"[DEBUG] Application exited with code: {code}")
                        sys.exit(code)
                    print(res)
                    stdout.append(res)
    except FileNotFoundError:
        print(f"Cannot open file {fileName}. File does not exist.")
    finally:
        if input_simulate_file:
            sys.stdin.close()
        if returnOutput:
            return stdout

if __name__ == "__main__":
    is_in_named_arguments = False
    input_file = ""
    textfiletosimulate = None
    # Parse flags and named command line arguments
    for i in argv:
        if i in ("-i", "--input"):
            is_in_named_arguments = "-i"
            continue
        if i in ("--simulate-input-from-text-file", "-textsiminput"):
            is_in_named_arguments = "-textsiminput"
            continue
        if i == "--release-mode":
            STORYSCRIPT_INTERPRETER_DEBUG_MODE = False
        elif i == "--debug-mode":
            STORYSCRIPT_INTERPRETER_DEBUG_MODE = True
        if is_in_named_arguments:
            if is_in_named_arguments == "-i":
                input_file = i
            elif is_in_named_arguments == "-textsiminput":
                textfiletosimulate = i
            is_in_named_arguments = False
    parse_file(input_file, textfiletosimulate)
