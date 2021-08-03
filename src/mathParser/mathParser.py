from .tokens import TokenType
from . import nodes

# [DevNote] Math process:
# In parenthesis Expression
# Powering
# Divide/Multiply/Modulo
# Add/Subtract


class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.advance()

    @staticmethod
    def raise_error():
        raise SyntaxError

    def advance(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def parse(self):
        if self.current_token is None:
            return None

        result = self.expr()

        if self.current_token is not None:
            self.raise_error()

        return result

    def expr(self):
        result = self.term()

        while self.current_token is not None and self.current_token.type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            if self.current_token.type == TokenType.PLUS:
                self.advance()
                result = nodes.AddNode(result, self.term())
            elif self.current_token.type == TokenType.MINUS:
                self.advance()
                result = nodes.SubtractNode(result, self.term())

        return result

    def term(self):
        result = self.factor()

        while self.current_token is not None and self.current_token.type in (
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
            TokenType.MODULO,
            TokenType.POWER,
        ):
            if self.current_token.type == TokenType.MULTIPLY:
                self.advance()
                result = nodes.MultiplyNode(result, self.factor())
            elif self.current_token.type == TokenType.DIVIDE:
                self.advance()
                result = nodes.DivideNode(result, self.factor())
            elif self.current_token.type == TokenType.MODULO:
                self.advance()
                result = nodes.ModuloNode(result, self.factor())
            elif self.current_token.type == TokenType.POWER:
                self.advance()
                result = nodes.PowerNode(result, self.factor())

        return result

    def factor(self):
        token = self.current_token

        if token.type == TokenType.LPAREN:
            self.advance()
            result = self.expr()

            if self.current_token.type != TokenType.RPAREN:
                self.raise_error()

            self.advance()
            return result
        if token.type == TokenType.NUMBER:
            self.advance()
            return nodes.NumberNode(token.value)
        if token.type == TokenType.STRING:
            self.advance()
            return nodes.StringNode(token.value)
        if token.type == TokenType.PLUS:
            self.advance()
            return nodes.PlusNode(self.factor())
        if token.type == TokenType.MINUS:
            self.advance()
            return nodes.MinusNode(self.factor())

        self.raise_error()
