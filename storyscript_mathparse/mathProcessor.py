from storyscript_mathparse.mathLexer import MathLexer
from storyscript_mathparse.mathParser import Parser
from storyscript_mathparse.mathInterpreter import Interpreter
from storyscript_mathparse.values import String


def process(expr, symbol_table):
    lexer = MathLexer(expr, symbol_table)
    tokens = lexer.generatetokens()
    parser = Parser(tokens)
    tree = parser.parse()
    interpreter = Interpreter()
    value = interpreter.visit(tree)
    if isinstance(value, String):
        return String(f"{value}"), None
    return value, None
