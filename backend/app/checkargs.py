import re as Regex


def areStr(map: dict, attrs: list):
    for k in attrs:
        if not isinstance(map[k], str):
            # print('type error: ' + k + f', type is: {type(map[k])}, value is {map[k]}')
            return False
    return True


def isStr(v):
    return isinstance(v, str)


def areInt(map: dict, attrs: list):
    for k in attrs:
        if not isinstance(map[k], int):
            # print('type error: ' + k + f', type is: {type(map[k])}, value is {map[k]}')
            return False
    return True


def isInt(a):
    return isinstance(a, int)


def areUint64(map: dict, attrs: list):
    for k in attrs:
        if not isinstance(map[k], int):
            return False
        if map[k] < 0 or map[k] > (1 << 65) - 1:
            return False
    return True


def isUint64(a):
    if not isInt(a):
        return False
    if a < 0 or a > (1 << 65) - 1:
        return False
    return True


def areBool(map: dict, attrs: list):
    for k in attrs:
        if not isinstance(map[k], bool):
            # print('type error: ' + k + f', type is: {type(map[k])}, value is {map[k]}')
            return False
    return True


def hasAttrs(map: dict, attrs: list):
    for k in attrs:
        if k not in map:
            return False
    return True


def isUrl(url):
    return Regex.match(r"https?://.+", url)


def isDate(s: str):
    return Regex.match(r"\d{4}-\d{1,2}-\d{1,2}", s)


def isSchoolId(s: str):
    return Regex.match(r"^\d{10}$", s)


def isClazz(s: str):
    return Regex.match(r"^未央-.+\d\d$", s)


def isPowOf2(a):
    while a & 1 == 0:
        a >>= 1
    return a == 1


def isDict(a):
    return isinstance(a, dict)