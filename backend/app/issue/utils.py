from .types import Visibility

from flask import g

from typing import List


def _split(string: str, sep: str = ";") -> List[str]:
    arr = string.split(sep)
    arr = filter(lambda x: x, arr)
    return list(arr)


def _am_admin() -> bool:
    from app.auth import challengeScope

    return challengeScope(["profile admin", "profile dayi"])


def _try_modify_visibility(visibility: str, author: str = None) -> Visibility:
    author = author or g.openid
    if visibility == Visibility.PUBLIC:
        if _am_admin():
            return Visibility.PUBLIC
        else:
            return Visibility.PROTECTED
    else:
        return Visibility(visibility)
