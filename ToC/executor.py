from langEnums import Types, Exceptions

class Executor:
	def __init__(self, symbol_table):
		self.symbol_table = symbol_table

	def check_is_float(self, command):
		is_float = False
		if(not isinstance(command, str)):
			command = str(command)
		for i in command:
			for j in i:
				if j == ".":
					is_float = True
					break
		return is_float

	def try_parse_int(self, val):
		try:
			return int(val)
		except ValueError:
			return val

	def add(self, command, keep_float):
		""" Adding numbers. """
		is_float = self.check_is_float(command)

		try:
			try:
				if(is_float):
					return float(command[0]) + float(command[2])
				return int(command[0]) + int(command[2])
			except ValueError:
				allvar = self.symbol_table.GetAllVariableName()
				is_string = False
				for i in command:
					if i.startswith('"') or i.endswith('"'):
						is_string = True
					if i in allvar:
						if self.symbol_table.GetVariableType(i) == Types.String:
							is_string = True
				if(command[0].startswith('"') or is_string):
					# String addition
					res = ""
					for i in command: # Find the Start and End of a String and add them together
						outword = i
						if i in allvar:
							outword = self.symbol_table.GetVariable(i)[1]
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
					is_float = self.check_is_float(self.symbol_table.GetVariable(command[0])) or self.check_is_float(self.symbol_table.GetVariable(command[2])) # Check If the Addition is Float or not
					
					c0var = self.symbol_table.GetVariable(command[0])[1] # Store command index 0 variable value
					c2var = self.symbol_table.GetVariable(command[2])[1] # Store command index 2 variable value
					
					if(is_float): # Check If the expression is float or not
						if(not keep_float): # Check If the keep_float boolean is False or not
							return self.try_parse_int(float(c0var) + float(c2var)) # Add 2 variable together and Try parse it as int
						return float(c0var) + float(c2var) # Add 2 variable together and return it as float
					return int(c0var) + int(c2var) # Add 2 variable together and return it as int
				elif(command[0] in allvar): # Check If command index 0 is a variable
					is_float = self.check_is_float(self.symbol_table.GetVariable(command[0])) or is_float # Check If the Addition is Float or not.
					c0var = self.symbol_table.GetVariable(command[0])[1] # Store command 0 variable value
					
					if(is_float): # Check If the expression is float or not
						if(not keep_float): # Check If the keep_float boolean is False or not
							return self.try_parse_int(float(c0var) + float(command[2])) # Add 2 variable together and Try parse it as int
						return float(c0var) + float(command[2]) # Add 2 variable together and return it as float
					return int(c0var) + int(command[2]) # Add 2 variable together and return it as int
				elif(command[2] in allvar): # Check If command index 2 is a variable
					is_float = self.check_is_float(self.symbol_table.GetVariable(command[2])) or is_float # Check If the addition is Float or not.
					c2var = self.symbol_table.GetVariable(command[2])[1] # Store command 2 variable value
					
					if(is_float): # Check If the expression is float or not
						if(not keep_float): # Check If the keep_float boolean is False or not
							return self.try_parse_int(float(c2var) + float(command[0])) # Add 2 variable together and Try parse it as int then return it.
						return float(c2var) + float(command[0]) # Add 2 variable together and return it as float
					return int(c2var) + int(command[0]) # Add 2 variable together and return it as int
		except IndexError:
			return Exceptions.InvalidSyntax # Return invalid syntax error if the expression is not completed.

	def subtract(self, command, keep_float):
		""" Subtract numbers. """
		is_float = self.check_is_float(command)

		try:
			try:
				if(is_float):
					return float(command[0]) - float(command[2])
				return int(command[0]) - int(command[2])
			except ValueError:
				allvar = self.symbol_table.GetAllVariableName()
				if((command[0] in allvar) and (command[2] in allvar)):
					is_float = self.check_is_float(self.symbol_table.GetVariable(command[0])) or self.check_is_float(self.symbol_table.GetVariable(command[2]))
					if(is_float):
						if(not keep_float):
							return self.try_parse_int(float(self.symbol_table.GetVariable(command[0])[1]) - float(self.symbol_table.GetVariable(command[2])[1]))
						return float(self.symbol_table.GetVariable(command[0])[1]) - float(self.symbol_table.GetVariable(command[2])[1])
					return int(self.symbol_table.GetVariable(command[0])[1]) - int(self.symbol_table.GetVariable(command[2])[1])
				elif(command[0] in allvar):
					is_float = self.check_is_float(self.symbol_table.GetVariable(command[0]))
					if(is_float):
						if(not keep_float):
							return self.try_parse_int(float(self.symbol_table.GetVariable(command[0])[1]) - float(command[2]))
						return float(self.symbol_table.GetVariable(command[0])[1]) - float(command[2])
					return int(self.symbol_table.GetVariable(command[0])[1]) - int(command[2])
				elif(command[2] in allvar):
					is_float = self.check_is_float(self.symbol_table.GetVariable(command[2]))
					if(is_float):
						if(not keep_float):
							return self.try_parse_int(float(self.symbol_table.GetVariable(command[2])[1]) - float(command[0]))
						return float(self.symbol_table.GetVariable(command[2])[1]) - float(command[0])
					return int(self.symbol_table.GetVariable(command[2])[1]) - int(command[0])
		except IndexError:
			return Exceptions.InvalidSyntax

	def multiply(self, command, keep_float):
		""" multiply numbers """
		is_float = self.check_is_float(command)

		try:
			try:
				# If both are normal numbers (Not variable)
				if(is_float):
					return float(command[0]) * float(command[2])
				return int(command[0]) * int(command[2])
			except ValueError:
				allvar = self.symbol_table.GetAllVariableName()
				if((command[0] in allvar) and (command[2] in allvar)):
					is_float = self.check_is_float(self.symbol_table.GetVariable(command[0])) or self.check_is_float(self.symbol_table.GetVariable(command[2]))
					if(is_float):
						if(not keep_float):
							return self.try_parse_int(float(self.symbol_table.GetVariable(command[0])[1]) * float(self.symbol_table.GetVariable(command[2])[1]))
						return float(self.symbol_table.GetVariable(command[0])[1]) * float(self.symbol_table.GetVariable(command[2])[1])
					return int(self.symbol_table.GetVariable(command[0])[1]) * int(self.symbol_table.GetVariable(command[2])[1])
				elif(command[0] in allvar):
					is_float = self.check_is_float(self.symbol_table.GetVariable(command[0]))
					if(is_float):
						if(not keep_float):
							return self.try_parse_int(float(self.symbol_table.GetVariable(command[0])[1]) * float(command[2]))
						return float(self.symbol_table.GetVariable(command[0])[1]) * float(command[2])
					return int(self.symbol_table.GetVariable(command[0])[1]) * int(command[2])
				elif(command[2] in allvar):
					is_float = self.check_is_float(self.symbol_table.GetVariable(command[2]))
					if(is_float):
						if(not keep_float):
							return self.try_parse_int(float(self.symbol_table.GetVariable(command[2])[1]) * float(command[0]))
						return float(self.symbol_table.GetVariable(command[2])[1]) * float(command[0])
					return int(self.symbol_table.GetVariable(command[2])[1]) * int(command[0])
		except IndexError:
			return Exceptions.InvalidSyntax

	def divide(self, command, keep_float):
		""" dividing numbers """
		is_float = self.check_is_float(command)

		try:
			try:
				if(is_float):
					return float(command[0]) / float(command[2])
				return int(command[0]) / int(command[2])
			except ValueError:
				allvar = self.symbol_table.GetAllVariableName()
				if((command[0] in allvar) and (command[2] in allvar)):
					is_float = self.check_is_float(self.symbol_table.GetVariable(command[0])) or self.check_is_float(self.symbol_table.GetVariable(command[2]))
					if(is_float):
						if(not keep_float):
							return self.try_parse_int(float(self.symbol_table.GetVariable(command[0])[1]) / float(self.symbol_table.GetVariable(command[2])[1]))
						return float(self.symbol_table.GetVariable(command[0])[1]) / float(self.symbol_table.GetVariable(command[2])[1])
					return int(self.symbol_table.GetVariable(command[0])[1]) / int(self.symbol_table.GetVariable(command[2])[1])
				elif(command[0] in allvar):
					is_float = self.check_is_float(self.symbol_table.GetVariable(command[0]))
					if(is_float):
						if(not keep_float):
							return self.try_parse_int(float(self.symbol_table.GetVariable(command[0])[1]) / float(command[2]))
						return float(self.symbol_table.GetVariable(command[0])[1]) / float(command[2])
					return int(self.symbol_table.GetVariable(command[0])[1]) / int(command[2])
				elif(command[2] in allvar):
					is_float = self.check_is_float(self.symbol_table.GetVariable(command[2]))
					if(is_float):
						if(not keep_float):
							return self.try_parse_int(float(self.symbol_table.GetVariable(command[2])[1]) / float(command[0]))
						return float(self.symbol_table.GetVariable(command[2])[1]) / float(command[0])
					return int(self.symbol_table.GetVariable(command[2])[1]) / int(command[0])
		except IndexError:
			return Exceptions.InvalidSyntax
		except ZeroDivisionError:
			return Exceptions.DivideByZeroException

	def pow(self, command, keep_float):
		""" Powering numbers """
		is_float = self.check_is_float(command)

		try:
			try:
				if(is_float):
					return float(command[0]) ** float(command[2])
				return int(command[0]) ** int(command[2])
			except ValueError:
				allvar = self.symbol_table.GetAllVariableName()
				if((command[0] in allvar) and (command[2] in allvar)):
					is_float = self.check_is_float(self.symbol_table.GetVariable(command[0])) or self.check_is_float(self.symbol_table.GetVariable(command[2]))
					if(is_float):
						if(not keep_float):
							return self.try_parse_int(float(self.symbol_table.GetVariable(command[0])[1]) ** float(self.symbol_table.GetVariable(command[2])[1]))
						return float(self.symbol_table.GetVariable(command[0])[1]) ** float(self.symbol_table.GetVariable(command[2])[1])
					return int(self.symbol_table.GetVariable(command[0])[1]) ** int(self.symbol_table.GetVariable(command[2])[1])
				elif(command[0] in allvar):
					is_float = self.check_is_float(self.symbol_table.GetVariable(command[0]))
					if(is_float):
						if(not keep_float):
							return self.try_parse_int(float(self.symbol_table.GetVariable(command[0])[1]) ** float(command[2]))
						return float(self.symbol_table.GetVariable(command[0])[1]) ** float(command[2])
					return int(self.symbol_table.GetVariable(command[0])[1]) ** int(command[2])
				elif(command[2] in allvar):
					is_float = self.check_is_float(self.symbol_table.GetVariable(command[2]))
					if(is_float):
						if(not keep_float):
							return self.try_parse_int(float(self.symbol_table.GetVariable(command[2])[1]) ** float(command[0]))
						return float(self.symbol_table.GetVariable(command[2])[1]) ** float(command[0])
					return int(self.symbol_table.GetVariable(command[2])[1]) ** int(command[0])
		except IndexError:
			return Exceptions.InvalidSyntax

	def modulo(self, command, keep_float):
		""" Adding numbers. """
		is_float = self.check_is_float(command)

		try:
			try:
				if(is_float):
					return float(command[0]) % float(command[2])
				return int(command[0]) % int(command[2])
			except ValueError:
				allvar = self.symbol_table.GetAllVariableName()
				if((command[0] in allvar) and (command[2] in allvar)): # Check If Command Index 0 and 2 are variables
					is_float = self.check_is_float(self.symbol_table.GetVariable(command[0])) or self.check_is_float(self.symbol_table.GetVariable(command[2])) # Check If the Addition is Float or not
					
					c0var = self.symbol_table.GetVariable(command[0])[1] # Store command index 0 variable value
					c2var = self.symbol_table.GetVariable(command[2])[1] # Store command index 2 variable value
					
					if(is_float): # Check If the expression is float or not
						if(not keep_float): # Check If the keep_float boolean is False or not
							return self.try_parse_int(float(c0var) % float(c2var)) # Add 2 variable together and Try parse it as int
						return float(c0var) % float(c2var) # Add 2 variable together and return it as float
					return int(c0var) % int(c2var) # Add 2 variable together and return it as int
				elif(command[0] in allvar): # Check If command index 0 is a variable
					is_float = self.check_is_float(self.symbol_table.GetVariable(command[0])) or is_float # Check If the Addition is Float or not.
					c0var = self.symbol_table.GetVariable(command[0])[1] # Store command 0 variable value
					
					if(is_float): # Check If the expression is float or not
						if(not keep_float): # Check If the keep_float boolean is False or not
							return self.try_parse_int(float(c0var) % float(command[2])) # Add 2 variable together and Try parse it as int
						return float(c0var) % float(command[2]) # Add 2 variable together and return it as float
					return int(c0var) % int(command[2]) # Add 2 variable together and return it as int
				elif(command[2] in allvar): # Check If command index 2 is a variable
					is_float = self.check_is_float(self.symbol_table.GetVariable(command[2])) or is_float # Check If the addition is Float or not.
					c2var = self.symbol_table.GetVariable(command[2])[1] # Store command 2 variable value
					
					if(is_float): # Check If the expression is float or not
						if(not keep_float): # Check If the keep_float boolean is False or not
							return self.try_parse_int(float(c2var) % float(command[0])) # Add 2 variable together and Try parse it as int then return it.
						return float(c2var) % float(command[0]) # Add 2 variable together and return it as float
					return int(c2var) % int(command[0]) # Add 2 variable together and return it as int
		except IndexError:
			return Exceptions.InvalidSyntax # Return invalid syntax error if the expression is not completed.