from .tokens import TokenType, Token
from string import ascii_letters

# Constants
WHITESPACE = " \n\t"
DIGITS = "0123456789"


class MathLexer:
    def __init__(self, text, symbol_table):
        self.original_text = text
        self.text = iter(text)
        self.current_character_index = 0
        self.symbol_table = symbol_table
        self.advance()

    def advance(self):
        try:
            self.current_character_index += 1
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
                if self.current_char == "/":
                    return
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
                self.advance()
                yield self.generate_string('"')
            elif self.current_char == "'":
                self.advance()
                yield self.generate_string("'")
            elif self.current_char == "~":
                self.advance()
                yield Token(TokenType.BITWISE_NOT)
            elif self.current_char == "&":
                self.advance()
                yield Token(TokenType.BITWISE_AND)
            elif self.current_char == "|":
                self.advance()
                yield Token(TokenType.BITWISE_OR)
            elif self.current_char == "^":
                self.advance()
                yield Token(TokenType.BITWISE_XOR)
            elif self.current_char == "<":
                self.advance()
                if self.current_char == "<":
                    self.advance()
                    yield Token(TokenType.BITWISE_LS)
                else:
                    raise SyntaxError(
                        "Comparison operator is not allowed in math expression yet."
                    )
            elif self.current_char == ">":
                self.advance()
                if self.current_char == ">":
                    self.advance()
                    yield Token(TokenType.BITWISE_RS)
                else:
                    raise SyntaxError(
                        "Comparison operator is not allowed in math expression yet."
                    )
            elif self.current_char in ascii_letters:
                for i in self.make_variable_name():
                    yield i
            else:
                raise SyntaxError(
                    f'Unknown character "{self.current_char}" in Math expression at character {self.current_character_index} in expression \"{self.original_text}\".'
                )

    def make_variable_name(self):
        variable_name = ""
        valid_variable_characters = ascii_letters + DIGITS + "_"

        while self.current_char is not None and (
            self.current_char in valid_variable_characters
        ):
            variable_name += self.current_char
            self.advance()

        variable_value = self.symbol_table.GetVariable(variable_name.strip())
        if not variable_value:
            raise NameError(f"Undefined variable \"{variable_name}\"")

        return list(MathLexer(str(variable_value[1]), self.symbol_table).generate_tokens())

    def generate_string(self, quote):
        inString = True
        outstr = ""

        while self.current_char is not None and inString:
            if self.current_char == "\\":
                self.advance()
                if self.current_char == "n":
                    outstr += "\n"
                elif self.current_char == "t":
                    outstr += "\t"
                elif self.current_char == "\\":
                    outstr += "\\"
                elif self.current_char == '"':
                    outstr += '"'
                elif self.current_char == "'":
                    outstr += "'"
                self.advance()
                continue
            if self.current_char == quote:
                self.advance()
                inString = False
                break
            outstr += self.current_char
            self.advance()

        return Token(TokenType.STRING, outstr)

    def generate_number(self):
        decimal_point_count = 0
        number_str = ""

        while self.current_char is not None and (
            self.current_char == "." or self.current_char in DIGITS
        ):
            if self.current_char == ".":
                decimal_point_count += 1
                if decimal_point_count > 1:
                    raise SyntaxError(f"Invalid floating point value \"{self.original_text}\"")

            number_str += self.current_char
            self.advance()

        if number_str.startswith("."):
            number_str = "0" + number_str
        if number_str.endswith("."):
            number_str += "0"

        return Token(TokenType.NUMBER, float(number_str))
