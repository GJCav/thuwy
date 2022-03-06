import requests

class ATManager():
    def __init__(self, appID, appSecret):
        self.appID = appID
        self.appSecret = appSecret

    def _getAccessToken(self):
        rtn = {}

        url = ("http://api.weixin.qq.com/cgi-bin/token?grant_type="
                "client_credential&appid=%s&secret=%s" % (self.appID, self.appSecret))
        res = requests.get(url).json()
        if res.has_key('access_token'):
            rtn['result'] = "succeeded."
            rtn['access_token'] = res['access_token']
        else:
            rtn['result'] = "failed."
            rtn.update(res)

        return rtn

    def getAccessToken(self):
        """
            a naive method to get access token
        """
        return self._getAccessToken()['access_token']
