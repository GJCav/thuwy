testCookieStr = """session=eyJfcGVybWFuZW50Ijp0cnVlLCJvcGVuaWQiOiJvdnRBQjU0NEg3dzJ6N0phNkNOYUNBWGtJU2VRIiwid3gtc2tleSI6Im4wdmNmRTJpVnUyNHg3VGpPaHN4S2c9PSJ9.Yf5GjA.V0g79-4gg1PAWJcofHBuCQmU180; Expires=Tue 08 Feb 2022 09:42:36 GMT; Secure; HttpOnly; Path=/; SameSite=None"""


cookieStr = """session=eyJvcGVuaWQiOiJvZHo0QjR4bFRnbEJaWGpHSVZoNjVhRnNpeUFZIiwid3gtc2tleSI6IloxLy92SWpPSUF3SWxjT1lMUnk5OXc9PSJ9.YRjPPw.7vAzce2sYdzbDe1AfI_4NKX0mR4; HttpOnly; Path=/"""

# headers = {"cookie": testCookieStr}
headers = {"Token": "gTBc5w6GK0ezTzE5y0tpoEHj"}

import requests as R


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

localTest = "http://127.0.0.1:5000/"
remoteTest = "http://api.weiyang.grw20.cn/"
baseUrl = localTest
