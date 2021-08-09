cookieStr = \
"""session=eyJvcGVuaWQiOiJvZHo0QjR4bFRnbEJaWGpHSVZoNjVhRnNpeUFZIiwid3gtc2tleSI6IjlWTjVsQ3d5dFlDbVl3NWdVOWZUelE9PSJ9.YRDhVw.5f0dKCB41eNxhHBKuF4ChFNCIYU; HttpOnly; Path=/"""


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