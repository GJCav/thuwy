"""
这个模块的所有 API 在返回 None 时，都表示有些地方出错了，且无法恢复
"""

import functools
import requests as R
from config import WX_APP_ID, WX_APP_SECRET
from app.ColorConsole import Red, Yellow
from datetime import datetime, timedelta

__token = {
    "token": "",
    "expire_at": datetime.fromtimestamp(0)
}


def updateToken() -> bool:
    """
    Update access token, return True if success or doing nothing, return False if an error occur
    """
    if datetime.now() < __token["expire_at"]:
        return True

    try:
        res = R.get("https://api.weixin.qq.com/cgi-bin/token?"
            + f"grant_type=client_credential&appid={WX_APP_ID}&secret={WX_APP_SECRET}")
        if res.status_code != 200:
            raise Exception(f"http code = {res.status_code}")
        
        json: dict = res.json()
        if not json:
            raise Exception("empty json payload")

        if "errcode" in json:
            raise Exception(f"wx errcode: {json['errcode']}")

        if "access_token" not in json:
            raise Exception(f"access token not found + {json}")

        __token["token"] = json["access_token"]
        __token["expire_at"] = datetime.now() + timedelta(seconds=json.get("expires_in", 7200) * 0.9)
        return True
    except Exception as e:
        print(f"{Yellow('wx_api')}: update access token error: " + Red(str(e)))
        return False


def __checkToken(handler):
    @functools.wraps(handler)
    def inner(*args, **kwargs):
        if __token["expire_at"] < datetime.now():
            if updateToken():
                return handler(*args, **kwargs)
            return None
        elif updateToken():
            return handler(*args, **kwargs)
        else:
            return None
    return inner


@__checkToken
def wx_getUnlimited(
    scene, 
    page=None, 
    check_path=True, 
    env_version="release",
    width=430
    ) -> R.Response or None:

    req_json = {
        "scene": scene,
        "check_path": check_path,
        "env_version": env_version,
        "width": width
    }
    if page:
        req_json["page"] = page

    try:
        token = __token["token"]
        res = R.post(f"https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token={token}", json=req_json)
        
        if res.status_code != 200:
            raise Exception(f"http error, code={res.status_code}")

        return res
    except Exception as e:
        print(Red("wx_api: wx_getUnlimited error") + ", " + str(e))