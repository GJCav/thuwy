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
        if k not in attrs: return False
    return True

def isUrl(url):
    return Regex.match(r'https?://.+', url)

