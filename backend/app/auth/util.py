import random
import string


def randomString(length: int) -> str:
    s = ""
    k = string.digits + string.ascii_letters
    for i in range(length):
        s += k[random.randint(0, len(k) - 1)]
    return s
