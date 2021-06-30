from mathParser.tokens import TokenType
from mathParser.nodes import *

# [DevNote] Math process:
# In parenthesis Expression
# Powering
# Divide/Multiply/Modulo
# Add/Subtract

class Parser:
	def __init__(self, tokens):
		self.tokens = iter(tokens)
		self.advance()

	def raise_error(self):
		raise SyntaxError

	def advance(self):
		try:
			self.current_token = next(self.tokens)
		except StopIteration:
			self.current_token = None

	def parse(self):
		if self.current_token == None:
			return None

		result = self.expr()

		if self.current_token is not None:
			self.raise_error()

		return result

	def expr(self):
		result = self.term()

		while self.current_token is not None and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
			if self.current_token.type == TokenType.PLUS:
				self.advance()
				result = AddNode(result, self.term())
			elif self.current_token.type == TokenType.MINUS:
				self.advance()
				result = SubtractNode(result, self.term())

		return result

	def term(self):
		result = self.factor()

		while self.current_token is not None and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
			if self.current_token.type == TokenType.MULTIPLY:
				self.advance()
				result = MultiplyNode(result, self.factor())
			elif self.current_token.type == TokenType.DIVIDE:
				self.advance()
				result = DivideNode(result, self.factor())
			elif self.current_token.type == TokenType.MODULO:
				self.advance()
				result = ModuloNode(result, self.factor())

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
		elif token.type == TokenType.NUMBER:
			self.advance()
			return NumberNode(token.value)
		elif token.type == TokenType.STRING:
			self.advance()
			return StringNode(token.value)
		elif token.type == TokenType.PLUS:
			self.advance()
			return PlusNode(self.factor())
		elif token.type == TokenType.MINUS:
			self.advance()
			return MinusNode(self.factor())

		self.raise_error()
