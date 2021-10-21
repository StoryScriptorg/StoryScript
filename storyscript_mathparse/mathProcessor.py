from .mathLexer import MathLexer
from .mathParser import Parser
from .mathInterpreter import Interpreter
from .values import String


def process(expr, symbol_table):
    lexer = MathLexer(expr, symbol_table)
    tokens = lexer.generate_tokens()
    parser = Parser(tokens)
    tree = parser.parse()
    interpreter = Interpreter()
    value = interpreter.visit(tree)
    if isinstance(value, String):
        return String(f"{value}"), None
    return value, None
