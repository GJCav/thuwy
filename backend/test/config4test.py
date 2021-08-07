cookieStr = \
"""session=eyJvcGVuaWQiOiJvZHo0QjR4bFRnbEJaWGpHSVZoNjVhRnNpeUFZIiwid3gtc2tleSI6Im1pNU5Qam5VeTBRWVFqSDVvb0d6YlE9PSJ9.YQ4WPQ.PDOjX2fHUK-sYkFq9VHK3CC0BiM"""

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