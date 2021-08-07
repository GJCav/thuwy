import re as Regex

def areStr(map: dict, attrs: list):
    for k in attrs:
        if not isinstance(map[k], str):
            # print('type error: ' + k + f', type is: {type(map[k])}, value is {map[k]}')
            return False
    return True

def areInt(map: dict, attrs: list):
    for k in attrs:
        if not isinstance(map[k], int):
            # print('type error: ' + k + f', type is: {type(map[k])}, value is {map[k]}')
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
        if k not in map: return False
    return True

def isUrl(url):
    return Regex.match(r'https?://.+', url)

def isDate(s: str):
    return Regex.match(r'\d{4}-\d{1,2}-\d{1,2}', s)

def isSchoolId(s: str):
    return Regex.match(r'^\d{10}$', s)

def isClazz(s: str):
    return Regex.match(r'^未央-.+\d\d$', s)

def isUint64(a):
    if a < 0 or a > (1<<65)-1: return False
    return True

def isPowOf2(a):
    while a & 1 == 0:
        a >>= 1
    return a == 1