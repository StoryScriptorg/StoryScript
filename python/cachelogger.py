from langEnums import Types
from orjson import dumps as dumpsjson, loads as loadsjson
from lexer import SymbolTable
from langParser import Parser
from executor import Executor

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
    def __init__(self, no_source=False):
        self.source_block = []
        self.no_source = no_source
        if self.no_source:
            self.source_block = ["#NOSOURCE"]
        self.cache_string = []

    def cache_var_declaration(self, vartype, name, value):
        # INT(TYPE) A(NAME) 5(VALUE)
        self.cache_string.append(f"{vartype} {name} {value}")

    def cache_var_set(self, varname, value):
        self.cache_string.append(f"SET {varname} {value}")

    def cache_function_call(self, funcname, args):
        self.cache_string.append(f"CALL {funcname} {args}")

    def cache_function_define(self, funcname, args, content):
        jsoncontent = dumpsjson({"args": args, "content": content}).decode("utf-8")
        self.cache_string.append(f"FUNC {funcname} [|!STARTCONTENT!|] {jsoncontent} [|!ENDCONTENT!|]")

    def cache_loopfor_loop(self, times, content):
        jsoncontent = dumpsjson({"content": content})
        self.cache_string.append(f"LOOPFOR {times} [|!STARTCONTENT!|] {jsoncontent} [|!ENDCONTENT!|]")

    def log_source(self, source):
        if not self.no_source:
            self.source_block.append(source)

    @staticmethod
    def retrieve_source(file_name, as_raw=False):
        with open(file_name,  'r') as file:
            content = file.readlines()
            res = []
            is_in_source_block = False
            for i in content:
                if i == "#NOSOURCE\n":
                    return None
                if i == "[SOURCE]\n":
                    is_in_source_block = True
                    continue
                if i == "[ENDSOURCE]\n":
                    is_in_source_block = False
                    break
                if is_in_source_block:
                    res.append(i)

            if as_raw:
                return "".join(res)

            return res

    @staticmethod
    def retrieve_cache(file_name, as_raw=False):
        with open(file_name, 'r') as file:
            content = file.readlines()
            res = []
            is_in_cache_block = False
            for i in content:
                if i == "[STARTCACHE]\n":
                    is_in_cache_block = True
                    continue
                if i == "[ENDCACHE]\n":
                    is_in_cache_block = False
                    break
                if is_in_cache_block:
                    res.append(i)

            if as_raw:
                return "".join(res)

            return res

    def save_cache(self, file_name):
        with open(file_name, 'w') as file:
            if self.source_block == ["#NOSOURCE"]:
                file.write("#NOSOURCE\n\n")
                file.writelines(self.cache_string)
            else:
                file.write("[SOURCE]\n")
                file.writelines(self.source_block)
                file.write("[ENDSOURCE]\n\n[STARTCACHE]\n")
                file.writelines(self.cache_string)
                file.write("\n[ENDCACHE]\n")

cachelogger = CacheLogger()
cachelogger.cache_var_declaration("int", "a", "10")
cachelogger.log_source("int a = 10\n")
cachelogger.save_cache("main_storyscript.stsc")
print("Cache:", cachelogger.retrieve_cache("main_storyscript.stsc", as_raw=False))
print("Source:", cachelogger.retrieve_source("main_storyscript.stsc", as_raw=False))

class CacheParser:
    def __init__(self, symbol_table, parser=None, executor=None):
        self.symbol_table = symbol_table
        self.parser = parser
        self.executor = executor

        if executor is None:
            self.executor = Executor(symbol_table)

        if parser is None:
            self.parser = Parser()

    def execute_cache(self, command):
        tc = command.split()

        if tc[0] in ["int", "bool", "float", "list", "dictionary", "tuple", "const", "string", "dynamic"]:
            # VARTYPE NAME VALUE:
            vartype = self.parser.parse_type_string(tc[0])
            is_keep_float = False
            if vartype == Types.Float:
                is_keep_float = True
            expr = self.parser.parse_expression(tc[2:], self.executor, is_keep_float)
            self.symbol_table.SetVariable(tc[1], (vartype, expr))
        elif tc[0] == "SET":
            # SET VARNAME VALUE:
            vartype = self.symbol_table.get_variable_type(tc[1])
            is_keep_float = False
            if vartype == Types.Float:
                is_keep_float = True
            expr = self.parser.parse_expression(tc[2:], self.executor, is_keep_float)
            self.symbol_table.SetVariable(tc[1], (vartype, expr))
        elif tc[0] == "CALL":
            if tc[1] == "print":
                print(self.execute_cache(self.parser.parse_string_list(tc[2:])[1:-1]))
            elif tc[1] == "input":
                return input(self.parser.parse_string_list(tc[2:])[1:-1])
        elif tc[0] == "FUNC":
            pass
        elif tc[0] == "LOOPFOR":
            if tc[1] in self.symbol_table.GetAllVariableName():
                tc[1] = self.symbol_table.GetVariable(tc[1])[1]
            times = int(tc[1])
            content = loadsjson(self.parser.parse_string_list(tc[3:-1]))
            loopcount = 0
            while loopcount < times:
                for i in content["content"]:
                    self.execute_cache(i)
                loopcount += 1
        else:
            return tc

if __name__ == "__main__":
    symboltable = SymbolTable()
    cacheParser = CacheParser(symboltable)
    cacheParser.execute_cache("LOOPFOR 10 [|!STARTCONTENT!|] {\"content\":[\"CALL print \\\"tong\\\"\"]} [|!ENDCONTENT!|]")
