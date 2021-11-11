def check_is_float_full_number(command) -> bool:
    res = safe_list_get(str(command).split("."), 1)
    return bool(res in (None, "0"))

def safe_list_get(alist: list, index: int):
    try:
        return alist[index]
    except IndexError:
        return None

def remove_string_postfix(msg: str, target: str) -> str:
    return msg[::-1].removeprefix(target)[::-1]

def remove_string_postfix_prefix(msg: str, target: str) -> str:
    return msg.removeprefix(target)[::-1].removeprefix(target)[::-1]
