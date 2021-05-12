class CommandTrimmer:
	def __init__(self):
		pass

	def analyseCommand(self, command):
		if command.endswith("\n"):
			command = command[:-1]
		res = command.split()
		return res

	def analyseCommands(self, commands):
		res = []
		for i in commands:
			if command.endswith("\n"):
				command = command[:-1]
			res.append(command.split())
		return res

class Executor:
	pass

class Interpreter:
	pass

def execute(command):
	trimmedCommand = CommandTrimmer().analyseCommand(command)
	return trimmedCommand

def parseFile(path):
	pass