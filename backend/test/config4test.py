cookieStr = \
"""session=eyJvcGVuaWQiOiJvZHo0QjR4bFRnbEJaWGpHSVZoNjVhRnNpeUFZIiwid3gtc2tleSI6IlkySm9UbFpsNUI1d0pJRmdjZXpqcUE9PSJ9.YRUByQ.J5UVsCgLiyrqa-zJS1f4u4-56dA; HttpOnly; Path=/"""


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