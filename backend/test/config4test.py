
localTest = "http://127.0.0.1:8989/"
remoteTest = "http://api.weiyang.grw20.cn/"
baseUrl = localTest

# headers = {"cookie": testCookieStr}
headers = {"cookie": ""}

import requests as R

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
        headers = {}


def _wrap(inner):
    def withHeader(*args, **kwargs):
        return inner(headers=headers, *args, **kwargs)

    return withHeader


R._get = R.get
R._post = R.post
R._delete = R.delete

R.get = _wrap(R.get)
R.post = _wrap(R.post)
R.delete = _wrap(R.delete)