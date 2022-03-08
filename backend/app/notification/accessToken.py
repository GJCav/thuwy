import requests
import datetime

def currentTime()->datetime:
    return datetime.datetime.now()

class ATManager():
    
    def __init__(self, appID, appSecret):
        self.appID = appID
        self.appSecret = appSecret
        self.tokenData = {}
        self.tokenData["access_token"] = ""
        self.tokenData["start_time"] = ""

    def _getAccessToken(self):
        rtn = {}
        print("call _getAccessToken()")
        url = ("http://api.weixin.qq.com/cgi-bin/token?grant_type="
                "client_credential&appid=%s&secret=%s" % (self.appID, self.appSecret))
        res = requests.get(url).json()
        self.tokenData["access_token"] = res['access_token']
        self.tokenData["start_time"] = currentTime().strftime('%Y-%m-%d %H:%M:%S')

        return 

    def getAccessToken(self):
        """
            a naive method to get access token
        """
        # return self._getAccessToken()['access_token']
        def tokenTimeOut():
            """check if token timed out"""
            curtime = currentTime()
            if self.tokenData["start_time"] == "":
                return True
            else:
                startTime = datetime.datetime.strptime(self.tokenData["start_time"], '%Y-%m-%d %H:%M:%S')
                passTime = curtime - startTime
                return passTime.seconds > 7000
        
        if self.tokenData["access_token"] == "" or tokenTimeOut():
            self._getAccessToken()
            
        return self.tokenData["access_token"]

        