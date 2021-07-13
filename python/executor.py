def check_is_float(command):
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
    if decimals != "0" and decimals:
        return True
    return False

def try_parse_int(val):
    try:
        return int(val)
    except ValueError:
        return val
