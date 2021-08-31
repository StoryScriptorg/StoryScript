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
    return bool(decimals != 0 and decimals)
