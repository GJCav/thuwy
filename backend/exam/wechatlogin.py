from flask import Flask, request, session, redirect
import requests as R
import json as Json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

WX_APP_ID = "wx7bfe035eee90419b"
WX_APP_SECRET = "51ed227eed49319fa6474bc79559dc2f"  # 生成环境中不会做明文储存


@app.route("/wxlogin/", methods=["POST"])
def wxlogin():
    data = request.get_json()
    if data and "code" in data:
        # return {"code": 0, "errmsg": "success", "back": data['code']}
        res = R.get(
            f"https://api.weixin.qq.com/sns/jscode2session?"
            + f"appid={WX_APP_ID}&secret={WX_APP_SECRET}&"
            + f"js_code={data['code']}&grant_type=authorization_code",
            timeout=5,
        )

        if res.status_code != 200:
            return {
                "code": 1,
                "errmsg": "unable to call auth.code2Session",
                "httpstatus": res.status_code,
            }

        resJson = Json.loads(res.text)

        # code 和 errmsg 消息在请求成功时不会出现在json中，但nmd傻逼微信文档里面又是有的
        # https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/login/auth.code2Session.html

        if "errcode" in resJson and resJson["errcode"] != 0:
            return {"code": 1, "errmsg": "fuck wexin.", "weixin": resJson}

        # 开发环境中不要传输明文的 openid 和 session_key，用flask的session存在cookies中

        session["wx-session-key"] = resJson["session_key"]
        session["openid"] = resJson["openid"]
        print(f'openid: {resJson["openid"]}')
        # return {"code": 0, "errmsg": "success", "sk": resJson["session_key"], "id": resJson["openid"]}
        return {"code": 0, "errmsg": "success"}

    else:
        return {"code": 1, "errmsg": "no code"}


if __name__ == "__main__":
    app.run(debug=True)
