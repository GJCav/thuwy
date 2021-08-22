testCookieStr = \
"""session=eyJfcGVybWFuZW50Ijp0cnVlLCJvcGVuaWQiOiJvZHo0QjR4bFRnbEJaWGpHSVZoNjVhRnNpeUFZIiwid3gtc2tleSI6Imd1ZWZlK0tWRmduY0MxMDJjWkhnNkE9PSJ9.YSHiMA.fiHm3L3eH-6wXCoVdOt_UaaqP2g; Expires=Wed 25 Aug 2021 05:35:44 GMT; HttpOnly; Path=/"""

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