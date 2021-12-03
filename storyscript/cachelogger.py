from langEnums import Types
from orjson import dumps as dumpsjson, loads as loadsjson
from .SymbolTable import SymbolTable
from .langParser import Parser


class CacheLogger:
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
        """Cache a Variable set"""
        self.cache_string.append(f"SET {varname} {value}")

    def cache_function_call(self, funcname, args):
        """Cache a Function call"""
        args = dumpsjson({"args": args})
        self.cache_string.append(f"CALL {funcname} {args}")

    def cache_function_define(self, funcname, args, content):
        """Cache a Function define"""
        jsoncontent = dumpsjson({"args": args, "content": content}).decode("utf-8")
        self.cache_string.append(
            f"FUNC {funcname} [|!STARTCONTENT!|] {jsoncontent} [|!ENDCONTENT!|]"
        )

    def cache_loopfor_loop(self, times, content):
        """Cache a loopfor loop"""
        jsoncontent = dumpsjson({"content": content})
        self.cache_string.append(
            f"LOOPFOR {times} [|!STARTCONTENT!|] {jsoncontent} [|!ENDCONTENT!|]"
        )

    def cache_ternary(self, condition, truecase, falsecase):
        jsoncontent = dumpsjson(
            {"condition": condition, "truecase": truecase, "falsecase": falsecase}
        )
        self.cache_string.append(f"TERNARY {jsoncontent}")

    def log_source(self, source):
        """Add source to the Source list."""
        if not self.no_source:
            self.source_block.append(source)

    @staticmethod
    def retrieve_source(file_name, as_raw=False):
        """Retrieve source from file specified"""
        with open(file_name, "r") as file:
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
        """Retrive a cache from a specified file"""
        with open(file_name, "r") as file:
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
        """Write the stored cache into a file specified."""
        with open(file_name, "w") as file:
            if self.source_block == ["#NOSOURCE"]:
                file.write("#NOSOURCE\n\n")
                file.writelines(self.cache_string)
            else:
                file.write("[SOURCE]\n")
                file.writelines(self.source_block)
                file.write("[ENDSOURCE]\n\n[STARTCACHE]\n")
                file.writelines(self.cache_string)
                file.write("\n[ENDCACHE]\n")


class CacheParser:
    def __init__(self, symbol_table, parser=None):
        self.symbol_table = symbol_table
        self.parser = parser

        if parser is None:
            self.parser = Parser(symbol_table)

    @staticmethod
    def trim_string(string):
        outstr = ""
        inString = False
        for i in string:
            if i == '"':
                inString = bool(not inString)
            if not inString and i == " ":
                continue
            outstr.append(i)
        return outstr

    def parse_function(self, tc):
        funclist = self.symbol_table.get_all_function_name()
        if tc[1] == "print":
            res = self.parser.parse_string_list(tc[2:])
            if res.endswith('"'):
                res = res[:-1]
            if res.startswith('"'):
                res = res[1:]
            res = self.execute_cache(res)
            print(res)
        elif tc[1] == "input":
            return input(self.parser.parse_string_list(tc[2:]))
        if tc[1] in funclist:
            funcObj = self.symbol_table.get_function(tc[1])
            args = self.parser.parse_string_list(tc[2:])
            args = self.trim_string(args)
            args = args.split("[||]")
            argslen = len(args) - 1
            i = 0
            while i < argslen:
                varobj = funcObj[0][i]
                varobj = varobj.split()
                self.symbol_table.SetVariable(varobj[1], args[i], varobj[0])
                i += 1
            for i in funcObj[1]:
                self.execute_cache(i)
            i = 0
            while i < argslen:
                varobj = (funcObj[0][i]).split()
                self.symbol_table.DeleteVariable(varobj[1])
                i += 1

    def execute_cache(self, command):
        tc = command.split()
        varlist = self.symbol_table.get_all_variable_name()

        if tc[0] in [
            "int",
            "bool",
            "float",
            "list",
            "dictionary",
            "tuple",
            "const",
            "string",
            "dynamic",
        ]:
            # VARTYPE NAME VALUE:
            vartype = self.parser.parse_type_string(tc[0])
            is_keep_float = False
            if vartype == Types.Float:
                is_keep_float = True
            expr = self.execute_cache(self.parser.parse_string_list(tc[2:]))
            self.symbol_table.SetVariable(tc[1], expr, vartype)
        elif tc[0] == "TERNARY":
            content = loadsjson(self.parser.parse_string_list(tc[1:]))
            print(content)
        elif tc[0] == "SET":
            # SET VARNAME VALUE:
            vartype = self.symbol_table.get_variable_type(tc[1])
            is_keep_float = False
            if vartype == Types.Float:
                is_keep_float = True
            expr = self.parser.parse_expression(tc[2:], is_keep_float)
            self.symbol_table.SetVariable(tc[1], expr, vartype)
        elif tc[0] == "CALL":
            return self.parse_function(tc)
        if tc[0] == "FUNC":
            loadedcontent = loadsjson(self.parser.parse_string_list(tc[2:]))
            self.symbol_table.setFunction(
                tc[1], loadedcontent["data"], loadedcontent["args"]
            )
        elif tc[0] == "LOOPFOR":
            if tc[1] in varlist:
                tc[1] = self.symbol_table.GetVariable(tc[1])[1]
            times = int(tc[1])
            content = loadsjson(self.parser.parse_string_list(tc[3:-1]))
            loopcount = 0
            while loopcount < times:
                for i in content["content"]:
                    self.execute_cache(i)
                loopcount += 1
        else:
            if tc[0] in varlist:
                return self.symbol_table.GetVariable(tc[0])[1]
            return self.parser.parse_string_list(tc)


if __name__ == "__main__":
    cachelogger = CacheLogger()
    cachelogger.cache_var_declaration("int", "a", "10")
    cachelogger.log_source("int a = 10\n")
    cachelogger.save_cache("main_storyscript.stsc")
    print("Cache:", cachelogger.retrieve_cache("main_storyscript.stsc", as_raw=False))
    print("Source:", cachelogger.retrieve_source("main_storyscript.stsc", as_raw=False))

    symboltable = SymbolTable()
    cacheParser = CacheParser(symboltable)
    cacheParser.execute_cache("int a 10")
    cacheParser.execute_cache("CALL print a")
    cacheParser.execute_cache("CALL print CALL input prompt hehe >\t")
    cacheParser.execute_cache(
        'TERNARY {"condition":"a == 5","truecase":["print (\\"The conditions is true.\\")"], "falsecase":[""]}'
    )
    cacheParser.execute_cache(
        'LOOPFOR 10 [|!STARTCONTENT!|] {"content":["CALL print \\"tong\\""]} [|!ENDCONTENT!|]'
    )
