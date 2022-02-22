
localTest = "http://127.0.0.1:8989/"
remoteTest = "https://dev-api.thuwy.top/"
baseUrl = localTest

# cookieStr 是以前的测试脚本需要使用的，这里保留一下
cookieStr = """"""
headers = {"cookie": cookieStr}

import requests as R
import functools

class UseAccount:
    def __init__(self, openid: str) -> None:
        self.openid = openid

    def __enter__(self):
        openid = self.openid

        res = R.get(f"{baseUrl}testaccount/{openid}/")
        assert res

        json = res.json()
        assert json["current"] == openid, f"测试账号切换错误，目标账号：{openid}，实际账号{json['current']}"

        global headers
        headers = {"cookie": f"session={res.cookies.get('session')}"}

    def __exit__(self, *args):
        global headers
        headers = {"cookie": cookieStr}


def _wrap(inner):
    @functools.wraps(inner)
    def withHeader(*args, **kwargs):
        return inner(headers=headers, *args, **kwargs)

    return withHeader


R._get = R.get
R._post = R.post
R._delete = R.delete

R.get = _wrap(R.get)
R.post = _wrap(R.post)
R.delete = _wrap(R.delete)