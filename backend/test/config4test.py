testCookieStr = \
"""session=eyJvcGVuaWQiOiJvZHo0QjR4bFRnbEJaWGpHSVZoNjVhRnNpeUFZIiwid3gtc2tleSI6IlkySm9UbFpsNUI1d0pJRmdjZXpqcUE9PSJ9.YRUByQ.J5UVsCgLiyrqa-zJS1f4u4-56dA; HttpOnly; Path=/"""

cookieStr = \
"""session=eyJvcGVuaWQiOiJvZHo0QjR4bFRnbEJaWGpHSVZoNjVhRnNpeUFZIiwid3gtc2tleSI6IjIxMlJZb2FkM1pTTHFVMkFWcmhRMUE9PSJ9.YRYiJg.Brhwo03DcgmgQXx1aBFBVdyRAAw; HttpOnly; Path=/"""


headers = {
    'cookie': cookieStr
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
baseUrl = remoteTest