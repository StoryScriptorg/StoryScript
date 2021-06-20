from langEnums import Types, Exceptions

class Executor:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    @staticmethod
    def check_is_float(command):
        is_float = False
        if not isinstance(command, str):
            command = str(command)
        isInDecimalsBlock = False
        decimals = ""
        for i in command:
            if i == ".":
                isInDecimalsBlock = True
                continue
            if isInDecimalsBlock:
                decimals += i
        if decimals != "0":
            if decimals:
                return True
        return False

    @staticmethod
    def try_parse_int(val):
        try:
            return int(val)
        except ValueError:
            return val

