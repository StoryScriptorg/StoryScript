import sys
from string import digits

from colorama import init, Fore, Style

from langData import Types
from lexer import Lexer, SymbolTable

GlobalVariableTable = SymbolTable()
init()


def execute(command, original_text: str = None):
    lexer = Lexer(GlobalVariableTable)
    return lexer.analyse_command(command.split(), original_text=original_text)[0]


STORYSCRIPT_INTERPRETER_DEBUG_MODE = True


def syntax_highlighting(statement):
    if isinstance(statement, str):
        statement = statement.split()
    if len(statement) == 0:
        return ""

    res = ""
    in_string = False
    for i in statement:
        i += " "
        out = i
        if i.startswith('"'):
            in_string = True
            out = Fore.GREEN + i
        elif in_string:
            if i.endswith('"'):
                in_string = False
            out = i
        elif i[:-1] in {
            "var",
            "int",
            "bool",
            "float",
            "list",
            "dictionary",
            "tuple",
            "const",
            "string",
            "dynamic",
        }:
            out = Fore.MAGENTA + i + Fore.RESET
        elif i[:-1] in {"print", "input", "exit"}:
            out = Fore.CYAN + i + Fore.RESET
        elif i[:-1] == "BREAKPOINT":
            out = Fore.RED + i + Fore.RESET
        else:
            sout = ""  # a Result string for the following for loop.
            for j in i:
                if j in digits:
                    sout += Fore.YELLOW + j
                elif j in {"+", "-", "*", "/", "**", "=", "+=", "-=", "/=", "%="}:
                    sout += Fore.RED + Style.BRIGHT + j
                else:
                    sout += j
            out = sout + Style.RESET_ALL
        res += out
    return res


class FileProcessor:
    def __init__(self):
        self.isBreakpoint = False

    def _handle_breakpoint(self, current_line):
        print(
            f"""{Style.BRIGHT}Breakpoint found! Please choose what to do next.{Style.RESET_ALL}
- one - Executing this and the next line and stop
- continue - Continue the execution until the Next Breakpoint or End of file
- exit - Stop the execution
Current line source:
    {syntax_highlighting(current_line)}"""
        )
        while True:
            continueChoice = input("(one/continue/exit) > ")
            if continueChoice == "exit":
                sys.exit(1)
            if continueChoice == "continue":
                self.isBreakpoint = False
                break
            if continueChoice == "one":
                self.isBreakpoint = True
                break
            print("Invalid choice!")

    def parse_file(self, fileName, input_simulate_file=None, returnOutput=False):
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
                    if commands and commands[0] == "BREAKPOINT" or self.isBreakpoint:
                        if STORYSCRIPT_INTERPRETER_DEBUG_MODE:
                            self._handle_breakpoint(i)
                            if commands[0] == "BREAKPOINT":
                                commands = commands[1:]
                        else:
                            print(
                                "WARNING: Breakpoint is ignored in Release mode. Please switch to debug mode to enable this feature."
                            )
                            commands = commands[1:]
                    res, error = (None, None)
                    try:
                        res, error = lexer.analyse_command(commands)
                    except Exception:  # skipcq: PYL-W0703
                        print("An exception occurred while executing the following line!")
                        from traceback import print_exc
                        print_exc()
                        print("Current line source:\n", commands)
                    if res is not None:
                        if res.startswith("EXITREQUEST"):
                            code = res.removeprefix("EXITREQUEST ")
                            try:
                                code = int(code)
                            except ValueError:
                                code = 0
                            if STORYSCRIPT_INTERPRETER_DEBUG_MODE:
                                print(f"[DEBUG] Application exited with code: {code}")
                            break
                        if error:
                            print(f"Current line source:\n\t{i}")
                        print(res)
                        stdout.append(res)
                        if error:
                            break
                if input_simulate_file:
                    sys.stdin.close()
                if returnOutput:
                    return stdout
        except FileNotFoundError:
            print(f"Cannot open file {fileName}. File does not exist.")
            if input_simulate_file:
                sys.stdin.close()
