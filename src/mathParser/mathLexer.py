from .tokens import TokenType, Token

# Constants
WHITESPACE = " \n\t"
DIGITS = "0123456789"


class MathLexer:
    def __init__(self, text):
        self.text = iter(text)
        self.advance()

    def advance(self):
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    def generate_tokens(self):
        while self.current_char is not None:
            if self.current_char in WHITESPACE:
                self.advance()
            elif self.current_char == "." or self.current_char in DIGITS:
                yield self.generate_number()
            elif self.current_char == "+":
                self.advance()
                yield Token(TokenType.PLUS)
            elif self.current_char == "-":
                self.advance()
                yield Token(TokenType.MINUS)
            elif self.current_char == "*":
                self.advance()
                if self.current_char == "*":
                    self.advance()
                    yield Token(TokenType.POWER)
                else:
                    yield Token(TokenType.MULTIPLY)
            elif self.current_char == "/":
                self.advance()
                yield Token(TokenType.DIVIDE)
            elif self.current_char == "%":
                self.advance()
                yield Token(TokenType.MODULO)
            elif self.current_char == "(":
                self.advance()
                yield Token(TokenType.LPAREN)
            elif self.current_char == ")":
                self.advance()
                yield Token(TokenType.RPAREN)
            elif self.current_char == '"':
                yield self.generate_string('"')
            elif self.current_char == "'":
                yield self.generate_string("'")
            else:
                raise SyntaxError(
                    f'Unknown character "{self.current_char}" in Math expression.'
                )

    def generate_string(self, quote):
        inString = True
        outstr = ""
        self.advance()

        while self.current_char is not None and inString:
            if self.current_char == quote:
                self.advance()
                inString = False
                break
            outstr += self.current_char
            self.advance()

        return Token(TokenType.STRING, outstr)

    def generate_number(self):
        decimal_point_count = 0
        number_str = self.current_char
        self.advance()

        while self.current_char is not None and (
            self.current_char == "." or self.current_char in DIGITS
        ):
            if self.current_char == ".":
                decimal_point_count += 1
                if decimal_point_count > 1:
                    break

            number_str += self.current_char
            self.advance()

        if number_str.startswith("."):
            number_str = "0" + number_str
        if number_str.endswith("."):
            number_str += "0"

        return Token(TokenType.NUMBER, float(number_str))
