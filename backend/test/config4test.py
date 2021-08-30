testCookieStr = \
"""session=eyJfcGVybWFuZW50Ijp0cnVlLCJvcGVuaWQiOiJvZHo0QjR4bFRnbEJaWGpHSVZoNjVhRnNpeUFZIiwid3gtc2tleSI6IkgxYlJkNm1nckxOQUFaZDdmTGdyWXc9PSJ9.YSuCNA.PHg2TuYLbRvl3ZzsIAf3YdTz0vk; Expires=Wed 01 Sep 2021 12:48:52 GMT; HttpOnly; Path=/"""

cookieStr = \
"""session=eyJvcGVuaWQiOiJvZHo0QjR4bFRnbEJaWGpHSVZoNjVhRnNpeUFZIiwid3gtc2tleSI6IloxLy92SWpPSUF3SWxjT1lMUnk5OXc9PSJ9.YRjPPw.7vAzce2sYdzbDe1AfI_4NKX0mR4; HttpOnly; Path=/"""

headers = {
    'cookie': testCookieStr
}


import requests as R
def _wrap(inner):
    def withHeader(*args, **kwargs):
        return inner(headers=headers, *args, **kwargs)
    return withHeader

R.get = _wrap(R.get)
R.post = _wrap(R.post)
R.delete = _wrap(R.delete)

localTest = 'http://127.0.0.1:5000/'
remoteTest = 'http://api.weiyang.grw20.cn/'
baseUrl = localTest