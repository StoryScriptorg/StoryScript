from mathParser.mathLexer import MathLexer
from mathParser.mathParser import Parser
from mathParser.mathInterpreter import Interpreter
from mathParser.values import String


def process(expr):
    lexer = MathLexer(expr)
    tokens = lexer.generate_tokens()
    parser = Parser(tokens)
    tree = parser.parse()
    if not tree:
        return
    interpreter = Interpreter()
    value = interpreter.visit(tree)
    return value


if __name__ == "__main__":
    print("StoryScript.python.math - Testing Shell")
    while True:
        print(process(input("StoryScript-MathParser > ")))
