from langEnums import Types
from lexer import Lexer, SymbolTable
import sys

GlobalVariableTable = SymbolTable()


def execute(command):
    trimmedCommand = command.split()

    lexer = Lexer(GlobalVariableTable)
    res = lexer.analyseCommand(trimmedCommand)[0]

    return res


STORYSCRIPT_INTERPRETER_DEBUG_MODE = True


def parse_file(fileName, input_simulate_file=None, returnOutput=False):
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

            if input_simulate_file:
                sys.stdin.close()
            if returnOutput:
                return stdout
    except FileNotFoundError:
        print(f"Cannot open file {fileName}. File does not exist.")
        if input_simulate_file:
            sys.stdin.close()
