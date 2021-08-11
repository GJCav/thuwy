cookieStr = \
"""session=eyJvcGVuaWQiOiJvZHo0QjR4bFRnbEJaWGpHSVZoNjVhRnNpeUFZIiwid3gtc2tleSI6InY1OXg1K1Ara3NlcktiUDlNQmVNWHc9PSJ9.YROCvQ.PYNg_J4rZkX7Gfk1D1SvoERx73E; HttpOnly; Path=/"""

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