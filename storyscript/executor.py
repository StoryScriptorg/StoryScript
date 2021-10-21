def check_is_float_full_number(command) -> bool:
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

def safe_list_get(alist: list, index: int):
    try:
        return alist[index]
    except IndexError:
        return None

def remove_string_postfix(msg: str, target: str):
    return msg[::-1].removeprefix(target)[::-1]

def remove_string_postfix_prefix(msg: str, target: str):
    return msg.removeprefix(target)[::-1].removeprefix(target)[::-1]
