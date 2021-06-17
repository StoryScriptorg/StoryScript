from langEnums import Types

"""
# [EXAMPLE TARGET CACHE FILE LAYOUT] #

[SOURCE]
int a = 10
print (a)
[ENDSOURCE]

[STARTCACHE]
INT A 10
PRINT A
[ENDCACHE]

If No source block:

#NOSOURCE
"""

class CacheLogger:
	def __init__(self, noSource=False):
		self.sourceBlock = []
		self.noSource = noSource
		if self.noSource:
			self.sourceBlock = ["#NOSOURCE"]
		self.cacheString = []

	def cacheVarDeclaration(self, vartype, name, value):
		# INT(TYPE) A(NAME) 5(VALUE)
		self.cacheString.append(f"{vartype} {name} {value}")

	def cacheVarSet(self, varname, value):
		self.cacheString.append(f"SET {varname} {value}")

	def cacheFunctionCall(self, funcname, args):
		self.cacheString.append(f"CALL {funcname} {args}")

	def cacheFunctionDefine(self, funcname, args, content):
		self.cacheString.append(f"FUNC {funcname} [|!STARTCONTENT!|] {content} [|!ENDCONTENT!|] [|!STARTARGS!|] {args} [|!ENDARGS!|]")

	def cacheLoopforLoop(self, times, content):
		self.cacheString.append(f"LOOPFOR {times} [|!STARTCONTENT!|] {content} [|!ENDCONTENT!|]")

	def logSource(self, source):
		if not self.noSource:
			self.sourceBlock.append(source)

	def retrieveSource(self, fileName, asRaw=False):
		file = open(fileName,  'r')
		content = file.readlines()
		res = []
		isInSourceBlock = False
		for i in content:
			if i == "#NOSOURCE\n":
				return None
			if i == "[SOURCE]\n":
				isInSourceBlock = True
				continue
			if i == "[ENDSOURCE]\n":
				isInSourceBlock = False
				break
			if isInSourceBlock:
				res.append(i)

		if asRaw:
			outstr = ""
			for i in res:
				outstr += i
			return outstr

		return res

	def retrieveCache(self, fileName, asRaw=False):
		file = open(fileName, 'r')
		content = file.readlines()
		res = []
		isInCacheBlock = False
		for i in content:
			if i == "[STARTCACHE]\n":
				isInCacheBlock = True
				continue
			if i == "[ENDCACHE]\n":
				isInCacheBlock = False
				break
			if isInCacheBlock:
				res.append(i)

		if asRaw:
			outstr = ""
			for i in res:
				outstr += i
			return outstr

		return res

	def saveCache(self, fileName):
		file = open(fileName, 'w')
		if self.sourceBlock == ["#NOSOURCE"]:
			file.write("#NOSOURCE\n\n")
			file.writelines(self.cacheString)
		else:
			file.write("[SOURCE]\n")
			file.writelines(self.sourceBlock)
			file.write("[ENDSOURCE]\n\n[STARTCACHE]\n")
			file.writelines(self.cacheString)
			file.write("\n[ENDCACHE]\n")

cachelogger = CacheLogger()
cachelogger.cacheVarDeclaration("int", "a", "10")
cachelogger.logSource("int a = 10\n")
cachelogger.saveCache("main_storyscript.stsc")
print("Cache:", cachelogger.retrieveCache("main_storyscript.stsc", asRaw=False))
print("Source:", cachelogger.retrieveSource("main_storyscript.stsc", asRaw=False))

class CacheParser:
	def __init__(self, symbolTable, parser, executor):
		self.symbolTable = symbolTable
		self.parser = parser
		self.executor = executor

	def executeCache(self, command):
		tc = tc.split()

		if tc[0] in ["int", "bool", "float", "list", "dictionary", "tuple", "const", "string", "dynamic"]:
			# VARTYPE NAME VALUE:
			vartype = parser.ParseTypeString(tc[0])
			isKeepFloat = False
			if vartype == Types.Float:
				isKeepFloat = True
			expr = parser.ParseExpression(tc[2:], self.executor, isKeepFloat)
			self.symbolTable.SetVariable(tc[1], (vartype, expr))
		elif tc[0] == "SET":
			# SET VARNAME VALUE:
			vartype = self.symbolTable.GetVariableType(tc[1])
			isKeepFloat = False
			if vartype == Types.Float:
				isKeepFloat = True
			expr = parser.ParseExpression(tc[2:], self.executor, isKeepFloat)
			self.symbolTable.SetVariable(tc[1], (vartype, expr))
		elif tc[0] == "CALL":
			pass
		elif tc[0] == "FUNC":
			pass
		elif tc[0] == "LOOPFOR":
			cacheParser = CacheParser()