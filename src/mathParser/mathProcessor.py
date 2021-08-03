from .mathLexer import MathLexer
from .mathParser import Parser
from .mathInterpreter import Interpreter
from .values import String


def process(expr):
    lexer = MathLexer(expr)
    tokens = lexer.generate_tokens()
    parser = Parser(tokens)
    tree = parser.parse()
    if not tree:
        return None, None
    interpreter = Interpreter()
    value = interpreter.visit(tree)
    if isinstance(value, String):
        return String(f"{value}"), None
    return value, None


if __name__ == "__main__":
    print("StoryScript.python.math - Testing Shell")
    while True:
        print(process(input("StoryScript-MathParser > ")))
