from filehelper import FileHelper
from langParser import Parser
from executor import Executor
from langEnums import Types, ConditionType, Exceptions
from string import ascii_letters
from random import randint

# This class is used to store variables and function
class SymbolTable:
	def __init__(self):
		self.variable_table = {"true":(Types.Boolean, 1), "false":(Types.Boolean, 0)}
		self.function_table = {}
		self.enableFunctionFeature = False
		self.ignoreInfo = False

	def copyvalue(self):
		return self.variable_table, self.function_table, self.enableFunctionFeature

	def importdata(self, variable_table, functionTable, enable_function_feature):
		self.variable_table = variable_table
		self.function_table = function_table
		self.enableFunctionFeature = enable_function_feature

	def get_all_variable_name(self):
		return self.variable_table.keys()

	def get_variable(self, key):
		return self.variable_table[key]

	def get_variable_type(self, key):
		return self.variable_table[key][0]

	def get_all_function_name(self):
		return self.function_table.keys()

	def get_function(self, key):
		return self.function_table[key]

	def set_variable(self, key, value, vartype, is_heap_allocated=False, str_size=None):
		self.variable_table[key] = (vartype, value, is_heap_allocated, str_size)

	def set_function(self, key, value, arguments):
		self.function_table[key] = (arguments, value)

	def delete_variable(self, key):
		del self.variable_table[key]

	def delete_function(self, key):
		del self.function_table[key]

global libraryIncluded
libraryIncluded:list = ["stdio.h", "stdlib.h"]

class Lexer:
	def __init__(self, symbol_table, out_file_name, parser=None, file_helper=None, auto_reallocate=True):
		self.symbol_table = symbol_table
		self.parser = parser
		self.file_helper = file_helper
		self.auto_reallocate = auto_reallocate

		if parser == None:
			self.parser = Parser()

		if fileHelper == None:
			self.file_helper = FileHelper(out_file_name)
			self.file_helper.insert_footer("\treturn 0;")
			self.file_helper.insert_footer("}")
			self.file_helper.indent_level = 1

	def throw_keyword(self, tc, multiple_commands_index, ln="Unknown"):
		# Throw keyword. "throw [Exception] [Description]"
		def getDescription():
			msg = ""
			for i in tc[2:multiple_commands_index + 1]:
				if i.startswith('"'):
					i = i[1:]
				if i.endswith('"'):
					i = i[:-1]
				msg += i + " "
			msg = msg[:-1]
			return self.parser.parse_escape_character(msg)
		if(tc[1] == "InvalidSyntax"):
			try:
				if(tc[2:multiple_commands_index + 1]):
					msg = getDescription()
					return f"raiseException(100, \"{msg}\");", ""
				else: raise IndexError
			except IndexError:
				return "raiseException(100, \"No Description provided\");", Exceptions.InvalidSyntax
		elif(tc[1] == "AlreadyDefined"):
			try:
				if(tc[2:multiple_commands_index + 1]):
					msg = getDescription()
					return f"raiseException(101, \"{msg}\");", Exceptions.AlreadyDefined
				else: raise IndexError
			except IndexError:
				return "raiseException(101, \"No Description provided\");", Exceptions.AlreadyDefined
		elif(tc[1] == "NotImplementedException"):
			try:
				if(tc[2:multiple_commands_index + 1]):
					msg = getDescription()
					return f"raiseException(102, \"{msg}\");", Exceptions.NotImplementedException
				else: raise IndexError
			except IndexError:
				return "raiseException(102, \"This feature is not implemented\");", Exceptions.NotImplementedException
		elif(tc[1] == "NotDefinedException"):
			try:
				if(tc[2:multiple_commands_index + 1]):
					msg = getDescription()
					return f"raiseException(103, \"{msg}\");", Exceptions.NotDefinedException
				else: raise IndexError
			except IndexError:
				return "raiseException(103, \"No Description provided\");", Exceptions.NotDefinedException
		elif(tc[1] == "GeneralException"):
			try:
				if(tc[2:multiple_commands_index + 1]):
					msg = getDescription()
					return f"raiseException(104, \"{msg}\");", Exceptions.GeneralException
				else: raise IndexError
			except IndexError:
				return "raiseException(104, \"No Description provided\");", Exceptions.GeneralException
		elif(tc[1] == "DivideByZeroException"):
			try:
				if(tc[2:multiple_commands_index + 1]):
					msg = getDescription()
					return f"raiseException(105, \"{msg}\");", Exceptions.DivideByZeroException
				else: raise IndexError
			except IndexError:
				return "raiseException(105, \"You cannot divide numbers with 0\");", Exceptions.DivideByZeroException
		elif(tc[1] == "InvalidValue"):
			try:
				if(tc[2:multiple_commands_index + 1]):
					msg = getDescription()
					return f"raiseException(106, \"{msg}\");", Exceptions.InvalidValue
				else: raise IndexError
			except IndexError:
				return "raiseException(106, \"No Description provided\");", Exceptions.InvalidValue
		elif(tc[1] == "InvalidTypeException"):
			try:
				if(tc[2:multiple_commands_index + 1]):
					msg = getDescription()
					return f"raiseException(107, \"{msg}\");", Exceptions.InvalidTypeException
				else: raise IndexError
			except IndexError:
				return "raiseException(107, \"No Description provided\");", Exceptions.InvalidTypeException
		else:
			self.raise_transpile_error("InvalidValue: The Exception entered is not defined", ln)

	def raise_transpile_error(self, text, ln="Unknown"):
		print("TRANSPILATION ERROR:")
		print(f"While processing line {ln}")
		print(text)
		raise SystemExit

	def variable_setting(self, tc, multiple_commands_index, ln):
		# Error messages
		invalid_value = "InvalidValue: Invalid value"
		mismatch_type = "InvalidValue: Value doesn't match variable type."

		if tc[1] == "=": # Set operator
			res, error = self.analyseCommand(tc[2:multiple_commands_index + 1])
			if error: return res, error
			value = ""

			for i in tc[2:multiple_commands_index + 1]:
				value += i + " "
			value = value[:-1]

			valtype = self.parser.parse_type_from_value(res)
			if valtype == Exceptions.InvalidSyntax:
				return invalid_value, Exceptions.InvalidValue
			vartype = self.symbol_table.get_variable_type(tc[0])
			# Check if Value Type matches Variable type
			if valtype != vartype:
				return mismatch_type, Exceptions.InvalidValue
			res = self.parser.parse_escape_character(res)
			if res in all_variable_name:
				res = (self.symbol_table.get_variable(res))[1]
			oldvar = self.symbol_table.get_variable(tc[0])
			if error: self.raise_transpile_error(error[0], ln)
			if oldvar[2]:
				if oldvar[0] == Types.String:
					error = self.symbol_table.set_variable(tc[0], res, vartype, oldvar[2], len(res) - 1)
					if self.auto_reallocate:
						if oldvar[3] < (len(res) - 1):
							self.file_helper.insert_content(f"{tc[0]} = realloc({tc[0]}, {len(res) - 1});")
						else:
							if oldvar[3] > len(res) - 1 and oldvar[3] > 64:
								self.file_helper.insert_content(f"{tc[0]} = realloc({tc[0]}, {len(res) - 1});")
					else:
						print("INFO: To set a Message to a String, Input string must be less than the Size specified or equal the Original string size If declared with initial value.")
						if lenght > oldvar[3]:
							self.raise_transpile_error("InvalidValue: The input string length is more than the Original Defined size. If you want a Dynamically allocated string, Please don't use \"--no-auto-reallocate\" option.", ln)
					return f"memcpy({tc[0]}, {res}, {len(res) - 1});", ""
				if oldvar[0] == Types.Dynamic:
					res = res.removeprefix("new Dynamic (")
					res = res[:-1]
					return f"{tc[0]} = (void*){res};", ""
				return f"*{tc[0]} = {res};", ""
			if vartype == Types.String:
				length = len(res) - 1
				error = self.symbol_table.set_variable(tc[0], res, vartype, oldvar[2], length)
				if length > oldvar[3]:
					self.raise_transpile_error("InvalidValue: The input string length is more than the Original Defined size. If you want a Dynamically allocated string, Please use the Heap allocated string instead If you want to make the String dynamiccally allocated.", ln)
				return f"memcpy({tc[0]}, {res}, {length});", ""
			if oldvar[0] == Types.Dynamic:
				res = res.removeprefix("new Dynamic (")
				res = res[:-1]
				return f"{tc[0]} = (void*){res};", ""
			error = self.symbol_table.set_variable(tc[0], res, vartype, oldvar[2])
			return f"{tc[0]} = {res};", ""
		elif tc[1] == "+=": # Add & Set operator
			res, error = self.analyseCommand(tc[2:multiple_commands_index + 1])
			if error: return res, error
			value = ""

			for i in tc[2:multiple_commands_index + 1]:
				value += i + " "
			value = value[:-1]

			valtype = self.parser.parse_type_from_value(res)
			if valtype == Exceptions.InvalidSyntax:
				return invalid_value, Exceptions.InvalidValue
			vartype = self.symbol_table.get_variable_type(tc[0])
			# Check if Value Type matches Variable type
			if valtype != vartype:
				return mismatch_type, Exceptions.InvalidValue
			res = self.parser.parse_escape_character(res)
			if res in all_variable_name:
				res = (self.symbol_table.get_variable(res))[1]
			oldvar = self.symbol_table.get_variable(tc[0])
			error = self.symbol_table.set_variable(tc[0], res, vartype, oldvar[2])
			if error: self.raise_transpile_error(error[0], ln)
			if oldvar[2]:
				if oldvar[0] == Types.String:
					self.raise_transpile_error("InvalidTypeException: You cannot use += with String.", ln)
				if oldvar[0] == Types.Dynamic:
					self.raise_transpile_error("InvalidTypeException: You cannot use += with Dynamics.", ln)
				return f"*{tc[0]} += {res};", ""
			return f"{tc[0]} += {res};", ""
		elif tc[1] == "-=": # Subtract & Set operator
			res, error = self.analyseCommand(tc[2:multiple_commands_index + 1])
			if error: return res, error
			value = ""

			for i in tc[2:multiple_commands_index + 1]:
				value += i + " "
			value = value[:-1]

			valtype = self.parser.parse_type_from_value(res)
			if valtype == Exceptions.InvalidSyntax:
				return invalid_value, Exceptions.InvalidValue
			vartype = self.symbol_table.get_variable_type(tc[0])
			# Check if Value Type matches Variable type
			if valtype != vartype:
				return mismatch_type, Exceptions.InvalidValue
			res = self.parser.parse_escape_character(res)
			if res in all_variable_name:
				res = (self.symbol_table.get_variable(res))[1]
			oldvar = self.symbol_table.get_variable(tc[0])
			error = self.symbol_table.set_variable(tc[0], res, vartype, oldvar[2])
			if error: self.raise_transpile_error(error[0], ln)
			if oldvar[2]:
				if oldvar[0] == Types.String:
					self.raise_transpile_error("InvalidTypeException: You cannot use -= with String.", ln)
				if oldvar[0] == Types.Dynamic:
					self.raise_transpile_error("InvalidTypeException: You cannot use -= with Dynamics.", ln)
				return f"*{tc[0]} -= {res};", ""
			return f"{tc[0]} -= {res};", ""
		elif tc[1] == "*=": # Multiply & Set operator
			res, error = self.analyseCommand(tc[2:multiple_commands_index + 1])
			if error: return res, error
			value = ""

			for i in tc[2:multiple_commands_index + 1]:
				value += i + " "
			value = value[:-1]

			valtype = self.parser.parse_type_from_value(res)
			if valtype == Exceptions.InvalidSyntax:
				return invalid_value, Exceptions.InvalidValue
			vartype = self.symbol_table.get_variable_type(tc[0])
			# Check if Value Type matches Variable type
			if valtype != vartype:
				return mismatch_type, Exceptions.InvalidValue
			res = self.parser.parse_escape_character(res)
			if res in all_variable_name:
				res = (self.symbol_table.get_variable(res))[1]
			oldvar = self.symbol_table.get_variable(tc[0])
			error = self.symbol_table.set_variable(tc[0], res, vartype, oldvar[2])
			if error: self.raise_transpile_error(error[0], ln)
			if oldvar[2]:
				if oldvar[0] == Types.String:
					self.raise_transpile_error("InvalidTypeException: You cannot use *= with String.", ln)
				if oldvar[0] == Types.Dynamic:
					self.raise_transpile_error("InvalidTypeException: You cannot use *= with Dynamics.", ln)
				return f"*{tc[0]} *= {res};", ""
			return f"{tc[0]} *= {res};", ""
		elif tc[1] == "/=": # Divide & Set operator
			res, error = self.analyseCommand(tc[2:multiple_commands_index + 1])
			if error: return res, error
			value = ""

			for i in tc[2:multiple_commands_index + 1]:
				value += i + " "
			value = value[:-1]

			valtype = self.parser.parse_type_from_value(res)
			if valtype == Exceptions.InvalidSyntax:
				return invalid_value, Exceptions.InvalidValue
			vartype = self.symbol_table.get_variable_type(tc[0])
			# Check if Value Type matches Variable type
			if valtype != vartype:
				return mismatch_type, Exceptions.InvalidValue
			res = self.parser.parse_escape_character(res)
			if res in all_variable_name:
				res = (self.symbol_table.get_variable(res))[1]
			oldvar = self.symbol_table.get_variable(tc[0])
			error = self.symbol_table.set_variable(tc[0], res, vartype, oldvar[2])
			if error: self.raise_transpile_error(error[0], ln)
			if oldvar[2]:
				if oldvar[0] == Types.String:
					self.raise_transpile_error("InvalidTypeException: You cannot use /= with String.", ln)
				if oldvar[0] == Types.Dynamic:
					self.raise_transpile_error("InvalidTypeException: You cannot use /= with Dynamics.", ln)
				return f"*{tc[0]} /= {res};", ""
			return f"{tc[0]} /= {res};", ""
		elif tc[1] == "%=": # Modulo Operaion & Set operator
			res, error = self.analyseCommand(tc[2:multiple_commands_index + 1])
			if error: return res, error
			value = ""

			for i in tc[2:multiple_commands_index + 1]:
				value += i + " "
			value = value[:-1]

			valtype = self.parser.parse_type_from_value(res)
			if valtype == Exceptions.InvalidSyntax:
				return invalid_value, Exceptions.InvalidValue
			vartype = self.symbol_table.get_variable_type(tc[0])
			# Check if Value Type matches Variable type
			if valtype != vartype:
				return mismatch_type, Exceptions.InvalidValue
			res = self.parser.parse_escape_character(res)
			if res in all_variable_name:
				res = (self.symbol_table.get_variable(res))[1]
			oldvar = self.symbol_table.get_variable(tc[0])
			error = self.symbol_table.set_variable(tc[0], res, vartype, oldvar[2])
			if error: self.raise_transpile_error(error[0], ln)
			if oldvar[2]:
				if oldvar[0] == Types.String:
					self.raise_transpile_error("InvalidTypeException: You cannot use %= with String.", ln)
				if oldvar[0] == Types.Dynamic:
					self.raise_transpile_error("InvalidTypeException: You cannot use %= with Dynamics.", ln)
				return f"*{tc[0]} %= {res};", ""
			return f"{tc[0]} %= {res};", ""
		else:
			res = ""
			for i in tc:
				res += i + " "
			res = res[:-1]
			return res, ""

	def switch_case_statement(self, tc, ln):
		cases = []
		case = []
		command = []
		isInCaseBlock = False
		isInDefaultBlock = False
		isAfterCaseKeyword = False
		currentCaseKey = None
		for i in tc[2:]:
			if i == "case":
				isAfterCaseKeyword = True
				continue
			if isAfterCaseKeyword:
				outkey = i
				if outkey.endswith(":"):
					outkey = outkey[:-1]
				currentCaseKey = outkey
				isAfterCaseKeyword = False
				isInCaseBlock = True
				continue
			if isInCaseBlock:
				if i == "&&":
					case.append(command)
					command = []
					continue
				if i == "break":
					case.append(command)
					cases.append((currentCaseKey, case))
					command = []
					case = []
					isInCaseBlock = False
					continue
				command.append(i)
			if i == "end":
				break

		defaultCase = False
		
		self.file_helper.insert_content(f"switch ({tc[1]})")
		self.file_helper.insert_content("{")
		self.file_helper.indent_level += 1
		for i in cases:
			if i[0] == "default":
				defaultCase = i
				continue
			self.file_helper.insert_content(f"case {i[0]}:")
			self.file_helper.indent_level += 1
			for j in i[1]:
				self.file_helper.insert_content(self.analyseCommand(j)[0])
			self.file_helper.insert_content("break;")
			self.file_helper.indent_level -= 1
		if defaultCase:
			self.file_helper.insert_content("default:")
			self.file_helper.indent_level += 1
			for j in i[1]:
				self.file_helper.insert_content(self.analyseCommand(j)[0])
			self.file_helper.insert_content("break;")
			self.file_helper.indent_level -= 1
		self.file_helper.indent_level -= 1
		self.file_helper.insert_content("}")

		return "", ""

	def if_else_statement(self, tc, ln):
		conditionslist:list = self.parser.parse_conditions(tc[1:])
		finalString = "if ("
		for i in conditionslist:
			exprs = []
			currentConditionType = ConditionType.Single
			for j in i:
				if j and isinstance(j, list):
					exprs.append(j)
				elif isinstance(j, ConditionType):
					currentConditionType = j
			if currentConditionType == ConditionType.And:
				for i in exprs:
					finalString += self.parser.parse_string_list(i) + " && "
				finalString = finalString[:-4]
			elif currentConditionType == ConditionType.Single:
				finalString += self.parser.parse_string_list(exprs[0])
			elif currentConditionType == ConditionType.Or:
				for i in exprs:
					finalString += self.parser.parse_string_list(i) + "||"
				finalString = finalString[:-4]
		finalString += ")"

		isInCodeBlock = False
		isInElseBlock = False
		have_passed_then_keyword = False
		ifstatement = {"if":[], "else":None}
		commands = []
		command = []
		endkeywordcount = 0 # All "end" keyword in the expression
		endkeywordpassed = 0 # All "end" keyword passed
		elsekeywordcount = 0 # All "else" keyword in the expression
		elsekeywordpassed = 0 # All "else" keyword passed
		for i in tc[2:]:
			if i == "end":
				endkeywordcount += 1
			elif i == "else":
				elsekeywordcount += 1
		for i in tc:
			if not have_passed_then_keyword and i == "then":
				isInCodeBlock = True
				have_passed_then_keyword = True
				continue
			if isInCodeBlock:
				if i == "&&":
					commands.append(command)
					command = []
					continue
				elif i == "end":
					endkeywordpassed += 1
					if endkeywordcount == endkeywordpassed:
						commands.append(command)
						command = []
						if isInElseBlock:
							ifstatement["else"] = commands
						else: ifstatement["if"] = commands
						isInElseBlock = False
						isInCodeBlock = False
						continue
				elif i == "else":
					elsekeywordpassed += 1
					if elsekeywordcount == elsekeywordpassed and endkeywordpassed + 1 == endkeywordcount:
						commands.append(command)
						command = []
						ifstatement["if"] = commands
						commands = []
						isInElseBlock = True
						continue
				command.append(i)
		self.file_helper.insert_content(finalString)
		self.file_helper.insert_content("{")
		self.file_helper.indent_level +=  1
		for i in ifstatement["if"]:
			self.file_helper.insert_content(self.analyseCommand(i)[0])
		self.file_helper.indent_level -= 1
		if ifstatement["else"] != None:
			self.file_helper.insert_content("} else {")
			self.file_helper.indent_level +=  1
			for i in ifstatement["else"]:
				self.file_helper.insert_content(self.analyseCommand(i)[0])
			self.file_helper.indent_level -= 1
			self.file_helper.insert_content("}")
		else: self.file_helper.insert_content("}")

		return "", ""

	def analyseCommand(self, tc, ln="Unknown", varcontext=None):
		# All Keywords
		basekeywords = ["if", "else", "var", "int",
						"bool", "float", "list", "dictionary",
						"tuple", "dynamic", "const", "override",
						"func", "end", "print", "input",
						"throw", "string", "del", "namespace",
						"#define", "loopfor", "switch",
						"input", "exit"]

		is_multiple_commands = False
		multiple_commands_index = -1
		for i in tc:
			multiple_commands_index += 1
			if i == "&&":
				is_multiple_commands = True
				break

		all_variable_name = self.symbol_table.get_all_variable_name()
		all_function_name = self.symbol_table.get_all_function_name()

		# Error messages
		paren_needed = "InvalidSyntax: Parenthesis is needed after a function name"
		close_paren_needed = "InvalidSyntax: Parenthesis is needed after an Argument input"

		try:
			if tc[0] in all_variable_name:
				try:
					return self.variable_setting(tc, multiple_commands_index, ln)
				except IndexError:
					res = ""
					for i in tc:
						res += i + " "
					res = res[:-1]
					return res, ""
			elif tc[0] in basekeywords:
				if tc[0] in ["var", "int", "bool", "float", "list", "dictionary", "tuple", "const", "string", "dynamic"]:
					try:
						if tc[2] == "=" or tc[3] == "=": pass
						else: raise IndexError
						definedType = self.parser.parse_type_string(tc[0])
						if(tc[1] in self.symbol_table.get_all_variable_name()):
							self.raise_transpile_error(f"AlreadyDefined: a Variable \"{tc[1]}\" is already defined", ln)
						
						# Checking for variable naming violation
						if not (self.parser.check_naming_violation(tc[1])):
							self.raise_transpile_error("InvalidValue: a Variable name cannot start with digits.", ln)

						# var(0) a(1) =(2) 3(3)
						# double(0) heap(1) b(2) =(3) 5(4)
						isHeap = False
						if tc[1] == "heap":
							isHeap = True
							res, error = self.analyseCommand(tc[4:multiple_commands_index + 1], tc[2])
							if isinstance(error, Exceptions):
								self.raise_transpile_error(res, ln)
						else:
							res, error = self.analyseCommand(tc[3:multiple_commands_index + 1], tc[1])
							if isinstance(error, Exceptions):
								self.raise_transpile_error(res, ln)
						value = ""

						for i in tc[3:multiple_commands_index + 1]:
							value += i + " "
						value = value[:-1]
						vartype = self.parser.parse_type_from_value(res)
						# Check If existing variable type matches the New value type
						if tc[0] != "var" and definedType != vartype:
							self.raise_transpile_error("InvalidValue: Variable types doesn't match value type.", ln)
						if vartype == Exceptions.InvalidSyntax:
							self.raise_transpile_error("InvalidSyntax: Invalid value", ln)
						res = self.parser.parse_escape_character(res)

						if isHeap:
							outvartype = tc[0]
							if tc[0] == "var":
								outvartype = self.parser.convert_types_enum_to_string(vartype)
							if vartype == Types.String:
								if "string.h" not in libraryIncluded:
									libraryIncluded.append("string.h")
								self.symbol_table.set_variable(tc[2], res, vartype, True, len(res) - 1)
								self.file_helper.insert_content(f"char *{tc[2]} = (char*)malloc({len(res) - 1});")
								return f"if({tc[2]} != NULL) memcpy({tc[2]}, {res}, {len(res) - 1});", ""
							if vartype == Types.Dynamic:
								# dynamic[0] heap[1] a[2] =[3] new[4] Dynamic[5] (memsize)[6]
								self.symbol_table.set_variable(tc[2], res, vartype, True)
								args = self.parser.parse_string_list(tc[6:])
								args = args[1:-1]
								varval = self.parser.parse_string_list(args)
								intval = self.parser.try_parse_int(varval)
								if isinstance(intval, int):
									if intval >= 2147483647 or intval <= -2147483647:
										if intval >= 9223372036854775807 or intval <= -9223372036854775807:
											bytesize = 16
										else: bytesize = 8
									else: bytesize = 4
								else:
									bytesize = len(varval) - 1
								try:
									self.file_helper.insert_content(f"void* {tc[2]} = malloc({bytesize});")
									return f"{tc[2]} = (void*){varval};", ""
								except NameError:
									return f"void* {tc[2]} = malloc({bytesize});"
							self.symbol_table.set_variable(tc[2], res, vartype, True)
							self.file_helper.insert_content(f"{outvartype} *{tc[2]} = ({outvartype}*)malloc(sizeof({outvartype}));")
							return f"*{tc[2]} = {res};", ""
						if tc[0] == "var":
							outvartype = self.parser.convert_types_enum_to_string(vartype)
							if vartype == Types.String:
								self.symbol_table.set_variable(tc[1], res, vartype, False, len(res) - 1)
								return f"char {tc[1]}[{len(res) - 1}] = {res};", ""
							if vartype == Types.Dynamic:
								# var[0] a[1] =[2] new[3] Dynamic[4] (memsize)[5]
								self.symbol_table.set_variable(tc[1], res, vartype, False)
								args = self.parser.parse_string_list(tc[5:])
								args = args[1:-1]
								varval = self.parser.parse_string_list(args)
								intval = self.parser.try_parse_int(varval)
								if isinstance(intval, int):
									if intval >= 2147483647 or intval <= -2147483647:
										if intval >= 9223372036854775807 or intval <= -9223372036854775807:
											bytesize = 16
										else: bytesize = 8
									else: bytesize = 4
								else:
									bytesize = len(varval) - 1
								return f"void* {tc[1]} = (void*){varval};", ""
							self.symbol_table.set_variable(tc[1], res, vartype, False)
							return f"{outvartype} {tc[1]} = {res};", ""
						if vartype == Types.String:
								self.symbol_table.set_variable(tc[1], res, vartype, False, len(res) - 1)
								return f"char {tc[1]}[{len(res) - 1}] = {res};", ""
						if vartype == Types.Dynamic:
							# dynamic[0] a[1] =[2] new[3] Dynamic[4] (memsize)[5]
							self.symbol_table.set_variable(tc[1], res, vartype, False)
							args = self.parser.parse_string_list(tc[5:])
							args = args[1:-1]
							varval = self.parser.parse_string_list(args)
							intval = self.parser.try_parse_int(varval)
							if isinstance(intval, int):
								if intval >= 2147483647 or intval <= -2147483647:
									if intval >= 9223372036854775807 or intval <= -9223372036854775807:
										bytesize = 16
									else: bytesize = 8
								else: bytesize = 4
							else:
								bytesize = len(varval) - 1
							return f"void* {tc[1]} = (void*){varval};", ""
						self.symbol_table.set_variable(tc[1], res, vartype, isHeap)
						return f"{tc[0]} {tc[1]} = {res};", ""
					except IndexError:
						# var(0) a(1)			(Stack allocation)
						# int(0) heap(1) a(2)	(Heap allocation)
						# string(0) heap(1) a(2) 20(3) (String heap allocation)
						if tc[0] == "var":
							print("[DEBUG]: Command:", tc)
							self.raise_transpile_error("InvalidSyntax: Initial value needed for var keyword", ln)
						vartype = self.parser.parse_type_string(tc[0])
						if vartype == Exceptions.InvalidSyntax:
							self.raise_transpile_error("InvalidSyntax: Invalid type", ln)
						if tc[1] == "heap":
							if vartype == Types.String:
								self.symbol_table.set_variable(tc[2], None, vartype, True, int(tc[3]))
								if "string.h" not in libraryIncluded:
									libraryIncluded.append("string.h")
								return f"char *{tc[2]} = (char*)malloc({tc[3]});", ""
							self.symbol_table.set_variable(tc[2], None, vartype, True)
							return f"{tc[0]} *{tc[2]} = ({tc[0]}*)malloc(sizeof({tc[0]}));", ""
						self.symbol_table.set_variable(tc[1], None, vartype, False)
						return f"{tc[0]} {tc[1]};", ""
				elif tc[0] == "print":
					value = ""
					for i in tc[1:multiple_commands_index + 1]:
						value += i + " "
					value = value[:-1]
					if not value.startswith('('): # Check If the expression has parentheses around or not
						return paren_needed, Exceptions.InvalidSyntax # Return error if not exists
					if not value.endswith(')'): # Check If the expression has parentheses around or not
						return close_paren_needed, Exceptions.InvalidSyntax # Return error if not exists
					value = value[1:-1]
					svalue = value.split()
					value = str(value)
					return f"printf({value});", None
				elif tc[0] == "input":
					value = ""
					for i in tc[2:multiple_commands_index + 1]: # Get all parameters provided as 1 long string
						value += i + " "
					value = value[:-1]
					if not value.startswith('('): # Check If the expression has parentheses around or not
						self.raise_transpile_error(paren_needed, ln) # Return error if not exists
					if not value.endswith(')'): # Check If the expression has parentheses around or not
						self.raise_transpile_error(close_paren_needed, ln) # Return error if not exists
					value = value[1:-1] # Cut parentheses out of the string
					return f"scanf(\"%s\", &{varcontext})", {int(tc[1])} # Return the Recieved Input
				elif tc[0] == "if":
					return self.if_else_statement(tc, ln)
				elif tc[0] == "exit":
					value = ""
					for i in tc[1:multiple_commands_index + 1]: # Get all parameters provided as 1 long string
						value += i + " "
					value = value[:-1]
					if not value.startswith('('): # Check If the expression has parentheses around or not
						self.raise_transpile_error(paren_needed, ln) # Return error if not exists
					if not value.endswith(')'): # Check If the expression has parentheses around or not
						self.raise_transpile_error(close_paren_needed, ln) # Return error if not exists
					value = value[1:-1]
					valtype = self.parser.parse_type_from_value(value)
					if value.startswith('"'):
						self.raise_transpile_error("InvalidValue: Exit code can only be integer.", ln)
					if value.endswith('"'):
						self.raise_transpile_error("InvalidValue: Exit code can only be integer.", ln)
					if not value:
						self.raise_transpile_error("InvalidValue: Parameter \"status\" (int) required.", ln)
					return f"exit({int(value)});", valtype
				elif tc[0] == "#define":
					try:
						if tc[1] == "interpet":
							# Set Interpreter Settings
							if tc[2] == "enableFunction":
								if tc[3] == "true":
									if not self.symbol_table.ignoreInfo:
										print("[DEBUG] INFO: Enable function")
									self.symbol_table.enableFunctionFeature = True
									return "", ""
								else:
									self.symbol_table.enableFunctionFeature = False
									return "", ""
							elif tc[2] == "ignoreInfo":
								if tc[3] == "true":
									self.symbol_table.ignoreInfo = True
									return "", ""
								else:
									print("[DEBUG] INFO: Ignore info disabled")
									self.symbol_table.ignoreInfo = False
									return "", ""
					except IndexError:
						self.raise_transpile_error("InvalidValue: You needed to describe what you will change.", ln)
				elif tc[0] == "throw":
					return self.throw_keyword(tc, multiple_commands_index) # Go to the Throw keyword function
				elif tc[0] == "del":
					if tc[1] not in all_variable_name:
						self.raise_transpile_error(f"NotDefinedException: The variable {tc[1]} is not defined.", ln)
					if not self.symbol_table.get_variable(tc[1])[2]:
						self.raise_transpile_error(f"InvalidValue: The variable {tc[1]} is not heap allocated.", ln)
					return f"free({tc[1]});", ""
				elif tc[0] == "func":
					if self.symbol_table.enableFunctionFeature:
						# func[0] Name[1] (arguments)[2]
						endIndex = -1
						for i in tc:
							endIndex += 1
							if i == "end":
								break

						if not tc[1] == "override":
							if tc[1] in all_function_name:
								return f"AlreadyDefined: The {tc[1]} function is already defined.", Exceptions.AlreadyDefined
						else:
							# func[0] override[1] Name[2] (arguments)[3]
							# Find all arguments declared.
							argumentsEndIndex = 1
							arguments = []
							isTypesKeywordFound = False
							for i in tc[2:endIndex]:
								argumentsEndIndex += 1
								if i.endswith(")"):
									break
							if not tc[2] in all_function_name:
								return f"NotDefinedException: The {tc[2]} function is not defined. You can't override non-existed function.", Exceptions.NotDefinedException
							else:
								self.symbol_table.set_function(tc[2], tc[argumentsEndIndex + 1:endIndex], tc[3:argumentsEndIndex - 1])
								return None, None
						# Find all arguments declared.
						argumentsEndIndex = 1
						arguments = []
						isTypesKeywordFound = False
						for i in tc[2:endIndex]:
							argumentsEndIndex += 1
							if i.endswith(")"):
								break
						self.symbol_table.set_function(tc[1], tc[argumentsEndIndex + 1:endIndex], arguments)
						return None, None
					else:
						return "This feature is disabled. Use \"#define interpet enableFunction true\" to enable this feature.", None
				elif tc[0] == "loopfor":
					try:
						commands = [] # list of commands
						command = []
						endkeywordcount = 0 # All "end" keyword in the expression
						endkeywordpassed = 0 # All "end" keyword passed
						for i in tc[2:]:
							if i == "end":
								endkeywordcount += 1
						for i in tc[2:]:
							if i == "&&":
								commands.append(command)
								command = []
								continue
							if i == "end":
								endkeywordpassed += 1
								if endkeywordcount == endkeywordpassed:
									commands.append(command)
									command = []
									break
							command.append(i)
						genvarname = None
						genvarname = "__sts_loopcount_"
						genvarname += ascii_letters[randint(0, 51)]
						genvarname += ascii_letters[randint(0, 51)]
						genvarname += ascii_letters[randint(0, 51)]
						self.file_helper.insert_content(f"for (int {genvarname} = 0; {genvarname} < {int(tc[1])}; {genvarname}++)" + " {")
						self.file_helper.indent_level += 1
						for i in commands:
							self.file_helper.insert_content(self.analyseCommand(i)[0])
						self.file_helper.indent_level -= 1
						self.file_helper.insert_content("}")
						return "", ""
					except ValueError:
						self.raise_transpile_error("InvalidValue: Count must be an Integer. (Whole number)", ln)
				elif tc[0] == "switch":
					return self.switch_case_statement(tc, ln)
				else:
					self.raise_transpile_error("NotImplementedException: This feature is not implemented", ln)
			elif tc[0] in all_function_name:
				return self.parser.parse_string_list(tc), ""
			elif tc[0] == "//":
				return self.parser.parse_string_list(tc), ""
			else:
				return self.parser.parse_string_list(tc), ""
		except IndexError:
			return "", ""