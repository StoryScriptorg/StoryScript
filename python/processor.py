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
        isBreakpoint = False
        with open(fileName, "r") as f:
            lexer = Lexer(GlobalVariableTable)
            lines = f.readlines()
            for i in lines:
                commands = i.split()
                if commands[0] == "BREAKPOINT" or isBreakpoint:
                    if STORYSCRIPT_INTERPRETER_DEBUG_MODE:
                        print(
f"""Breakpoint found! Please choose what to do next.
 - one - Executing this and the next line and stop
 - continue - Continue the execution until the Next Breakpoint or End of file
 - exit - Stop the execution
Current line source:
    {i}""")
                        continueChoice = input("(one/continue/exit) > ")
                        if continueChoice == "exit":
                            sys.exit(1)
                        if continueChoice == "continue":
                            isBreakpoint = False
                            if commands[0] == "BREAKPOINT":
                                commands = commands[1:]
                        if continueChoice == "one":
                            isBreakpoint = True
                            if commands[0] == "BREAKPOINT":
                                commands = commands[1:]
                    else:
                        print("WARNING: Breakpoint is ignored in Release mode. Please switch to debug mode to enable this feature.")
                        commands = commands[1:]
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
