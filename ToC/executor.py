from langEnums import *

class Executor:
	def __init__(self, symbolTable):
		self.symbolTable = symbolTable

	def CheckIsFloat(self, command):
		isFloat = False
		if(not isinstance(command, str)):
			command = str(command)
		for i in command:
			for j in i:
				if j == ".":
					isFloat = True
					break
		return isFloat

	def TryParseInt(self, val):
		try:
			return int(val)
		except ValueError:
			return val

	def add(self, command, keepFloat):
		""" Adding numbers. """
		isFloat = self.CheckIsFloat(command)

		try:
			try:
				if(isFloat):
					return float(command[0]) + float(command[2])
				else:
					return int(command[0]) + int(command[2])
			except ValueError:
				allvar = self.symbolTable.GetAllVariableName()
				isString = False
				for i in command:
					if i.startswith('"') or i.endswith('"'):
						isString = True
					if i in allvar:
						if self.symbolTable.GetVariableType(i) == Types.String:
							isString = True
				if(command[0].startswith('"') or isString):
					# String addition
					res = ""
					for i in command: # Find the Start and End of a String and add them together
						outword = i
						if i in allvar:
							outword = self.symbolTable.GetVariable(i)[1]
						if outword.startswith('"'):
							outword = outword[1:]
						if outword.endswith('"'):
							outword = outword[:-1]
						if i == "+":
							continue
						res += outword + " "

					res = res[:-1]

					return '"' + res + '"' # Return the result in quote to mark as String type
				elif((command[0] in allvar) and (command[2] in allvar)): # Check If Command Index 0 and 2 are variables
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0])) or self.CheckIsFloat(self.symbolTable.GetVariable(command[2])) # Check If the Addition is Float or not
					
					c0var = self.symbolTable.GetVariable(command[0])[1] # Store command index 0 variable value
					c2var = self.symbolTable.GetVariable(command[2])[1] # Store command index 2 variable value
					
					if(isFloat): # Check If the expression is float or not
						if(not keepFloat): # Check If the keepFloat boolean is False or not
							return self.TryParseInt(float(c0var) + float(c2var)) # Add 2 variable together and Try parse it as int
						else: return float(c0var) + float(c2var) # Add 2 variable together and return it as float
					else: return int(c0var) + int(c2var) # Add 2 variable together and return it as int
				elif(command[0] in allvar): # Check If command index 0 is a variable
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0])) or isFloat # Check If the Addition is Float or not.
					c0var = self.symbolTable.GetVariable(command[0])[1] # Store command 0 variable value
					
					if(isFloat): # Check If the expression is float or not
						if(not keepFloat): # Check If the keepFloat boolean is False or not
							return self.TryParseInt(float(c0var) + float(command[2])) # Add 2 variable together and Try parse it as int
						else: return float(c0var) + float(command[2]) # Add 2 variable together and return it as float
					else: return int(c0var) + int(command[2]) # Add 2 variable together and return it as int
				elif(command[2] in allvar): # Check If command index 2 is a variable
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[2])) or isFloat # Check If the addition is Float or not.
					c2var = self.symbolTable.GetVariable(command[2])[1] # Store command 2 variable value
					
					if(isFloat): # Check If the expression is float or not
						if(not keepFloat): # Check If the keepFloat boolean is False or not
							return self.TryParseInt(float(c2var) + float(command[0])) # Add 2 variable together and Try parse it as int then return it.
						else: float(c2var) + float(command[0]) # Add 2 variable together and return it as float
					else: return int(c2var) + int(command[0]) # Add 2 variable together and return it as int
		except IndexError:
			return Exceptions.InvalidSyntax # Return invalid syntax error if the expression is not completed.

	def subtract(self, command, keepFloat):
		""" Subtract numbers. """
		isFloat = self.CheckIsFloat(command)

		try:
			try:
				if(isFloat):
					return float(command[0]) - float(command[2])
				else:
					return int(command[0]) - int(command[2])
			except ValueError:
				allvar = self.symbolTable.GetAllVariableName()
				if((command[0] in allvar) and (command[2] in allvar)):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0])) or self.CheckIsFloat(self.symbolTable.GetVariable(command[2]))
					if(isFloat):
						if(not keepFloat):
							return self.TryParseInt(float(self.symbolTable.GetVariable(command[0])[1]) - float(self.symbolTable.GetVariable(command[2])[1]))
						else: return float(self.symbolTable.GetVariable(command[0])[1]) - float(self.symbolTable.GetVariable(command[2])[1])
					else: return int(self.symbolTable.GetVariable(command[0])[1]) - int(self.symbolTable.GetVariable(command[2])[1])
				elif(command[0] in allvar):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0]))
					if(isFloat):
						if(not keepFloat):
							return self.TryParseInt(float(self.symbolTable.GetVariable(command[0])[1]) - float(command[2]))
						else: return float(self.symbolTable.GetVariable(command[0])[1]) - float(command[2])
					else: return int(self.symbolTable.GetVariable(command[0])[1]) - int(command[2])
				elif(command[2] in allvar):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[2]))
					if(isFloat):
						if(not keepFloat):
							return self.TryParseInt(float(self.symbolTable.GetVariable(command[2])[1]) - float(command[0]))
						else: float(self.symbolTable.GetVariable(command[2])[1]) - float(command[0])
					else: return int(self.symbolTable.GetVariable(command[2])[1]) - int(command[0])
		except IndexError:
			return Exceptions.InvalidSyntax

	def multiply(self, command, keepFloat):
		""" multiply numbers """
		isFloat = self.CheckIsFloat(command)

		try:
			try:
				# If both are normal numbers (Not variable)
				if(isFloat):
					return float(command[0]) * float(command[2])
				else:
					return int(command[0]) * int(command[2])
			except ValueError:
				allvar = self.symbolTable.GetAllVariableName()
				if((command[0] in allvar) and (command[2] in allvar)):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0])) or self.CheckIsFloat(self.symbolTable.GetVariable(command[2]))
					if(isFloat):
						if(not keepFloat):
							return self.TryParseInt(float(self.symbolTable.GetVariable(command[0])[1]) * float(self.symbolTable.GetVariable(command[2])[1]))
						else: return float(self.symbolTable.GetVariable(command[0])[1]) * float(self.symbolTable.GetVariable(command[2])[1])
					else: return int(self.symbolTable.GetVariable(command[0])[1]) * int(self.symbolTable.GetVariable(command[2])[1])
				elif(command[0] in allvar):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0]))
					if(isFloat):
						if(not keepFloat):
							return self.TryParseInt(float(self.symbolTable.GetVariable(command[0])[1]) * float(command[2]))
						else: return float(self.symbolTable.GetVariable(command[0])[1]) * float(command[2])
					else: return int(self.symbolTable.GetVariable(command[0])[1]) * int(command[2])
				elif(command[2] in allvar):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[2]))
					if(isFloat):
						if(not keepFloat):
							return self.TryParseInt(float(self.symbolTable.GetVariable(command[2])[1]) * float(command[0]))
						else: float(self.symbolTable.GetVariable(command[2])[1]) * float(command[0])
					else: return int(self.symbolTable.GetVariable(command[2])[1]) * int(command[0])
		except IndexError:
			return Exceptions.InvalidSyntax

	def divide(self, command, keepFloat):
		""" dividing numbers """
		isFloat = self.CheckIsFloat(command)

		try:
			try:
				if(isFloat):
					return float(command[0]) / float(command[2])
				else:
					return int(command[0]) / int(command[2])
			except ValueError:
				allvar = self.symbolTable.GetAllVariableName()
				if((command[0] in allvar) and (command[2] in allvar)):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0])) or self.CheckIsFloat(self.symbolTable.GetVariable(command[2]))
					if(isFloat):
						if(not keepFloat):
							return self.TryParseInt(float(self.symbolTable.GetVariable(command[0])[1]) / float(self.symbolTable.GetVariable(command[2])[1]))
						else: return float(self.symbolTable.GetVariable(command[0])[1]) / float(self.symbolTable.GetVariable(command[2])[1])
					else: return int(self.symbolTable.GetVariable(command[0])[1]) / int(self.symbolTable.GetVariable(command[2])[1])
				elif(command[0] in allvar):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0]))
					if(isFloat):
						if(not keepFloat):
							return self.TryParseInt(float(self.symbolTable.GetVariable(command[0])[1]) / float(command[2]))
						else: return float(self.symbolTable.GetVariable(command[0])[1]) / float(command[2])
					else: return int(self.symbolTable.GetVariable(command[0])[1]) / int(command[2])
				elif(command[2] in allvar):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[2]))
					if(isFloat):
						if(not keepFloat):
							return self.TryParseInt(float(self.symbolTable.GetVariable(command[2])[1]) / float(command[0]))
						else: float(self.symbolTable.GetVariable(command[2])[1]) / float(command[0])
					else: return int(self.symbolTable.GetVariable(command[2])[1]) / int(command[0])
		except IndexError:
			return Exceptions.InvalidSyntax
		except ZeroDivisionError:
			return Exceptions.DivideByZeroException

	def pow(self, command, keepFloat):
		""" Powering numbers """
		isFloat = self.CheckIsFloat(command)

		try:
			try:
				if(isFloat):
					return float(command[0]) ** float(command[2])
				else:
					return int(command[0]) ** int(command[2])
			except ValueError:
				allvar = self.symbolTable.GetAllVariableName()
				if((command[0] in allvar) and (command[2] in allvar)):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0])) or self.CheckIsFloat(self.symbolTable.GetVariable(command[2]))
					if(isFloat):
						if(not keepFloat):
							return self.TryParseInt(float(self.symbolTable.GetVariable(command[0])[1]) ** float(self.symbolTable.GetVariable(command[2])[1]))
						else: return float(self.symbolTable.GetVariable(command[0])[1]) ** float(self.symbolTable.GetVariable(command[2])[1])
					else: return int(self.symbolTable.GetVariable(command[0])[1]) ** int(self.symbolTable.GetVariable(command[2])[1])
				elif(command[0] in allvar):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0]))
					if(isFloat):
						if(not keepFloat):
							return self.TryParseInt(float(self.symbolTable.GetVariable(command[0])[1]) ** float(command[2]))
						else: return float(self.symbolTable.GetVariable(command[0])[1]) ** float(command[2])
					else: return int(self.symbolTable.GetVariable(command[0])[1]) ** int(command[2])
				elif(command[2] in allvar):
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[2]))
					if(isFloat):
						if(not keepFloat):
							return self.TryParseInt(float(self.symbolTable.GetVariable(command[2])[1]) ** float(command[0]))
						else: float(self.symbolTable.GetVariable(command[2])[1]) ** float(command[0])
					else: return int(self.symbolTable.GetVariable(command[2])[1]) ** int(command[0])
		except IndexError:
			return Exceptions.InvalidSyntax

	def modulo(self, command, keepFloat):
		""" Adding numbers. """
		isFloat = self.CheckIsFloat(command)

		try:
			try:
				if(isFloat):
					return float(command[0]) % float(command[2])
				else:
					return int(command[0]) % int(command[2])
			except ValueError:
				allvar = self.symbolTable.GetAllVariableName()
				if((command[0] in allvar) and (command[2] in allvar)): # Check If Command Index 0 and 2 are variables
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0])) or self.CheckIsFloat(self.symbolTable.GetVariable(command[2])) # Check If the Addition is Float or not
					
					c0var = self.symbolTable.GetVariable(command[0])[1] # Store command index 0 variable value
					c2var = self.symbolTable.GetVariable(command[2])[1] # Store command index 2 variable value
					
					if(isFloat): # Check If the expression is float or not
						if(not keepFloat): # Check If the keepFloat boolean is False or not
							return self.TryParseInt(float(c0var) % float(c2var)) # Add 2 variable together and Try parse it as int
						else: return float(c0var) % float(c2var) # Add 2 variable together and return it as float
					else: return int(c0var) % int(c2var) # Add 2 variable together and return it as int
				elif(command[0] in allvar): # Check If command index 0 is a variable
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[0])) or isFloat # Check If the Addition is Float or not.
					c0var = self.symbolTable.GetVariable(command[0])[1] # Store command 0 variable value
					
					if(isFloat): # Check If the expression is float or not
						if(not keepFloat): # Check If the keepFloat boolean is False or not
							return self.TryParseInt(float(c0var) % float(command[2])) # Add 2 variable together and Try parse it as int
						else: return float(c0var) % float(command[2]) # Add 2 variable together and return it as float
					else: return int(c0var) % int(command[2]) # Add 2 variable together and return it as int
				elif(command[2] in allvar): # Check If command index 2 is a variable
					isFloat = self.CheckIsFloat(self.symbolTable.GetVariable(command[2])) or isFloat # Check If the addition is Float or not.
					c2var = self.symbolTable.GetVariable(command[2])[1] # Store command 2 variable value
					
					if(isFloat): # Check If the expression is float or not
						if(not keepFloat): # Check If the keepFloat boolean is False or not
							return self.TryParseInt(float(c2var) % float(command[0])) # Add 2 variable together and Try parse it as int then return it.
						else: float(c2var) % float(command[0]) # Add 2 variable together and return it as float
					else: return int(c2var) % int(command[0]) # Add 2 variable together and return it as int
		except IndexError:
			return Exceptions.InvalidSyntax # Return invalid syntax error if the expression is not completed.