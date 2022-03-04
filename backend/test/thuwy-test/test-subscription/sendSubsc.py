import requests
from secret import OPEN_ID, WX_APP_ID, WX_APP_SECRET, SUBSC_TPL_ID
STATE_WAIT = 0b000001
STATE_START = 0b000010
STATE_COMPLETE = 0b000100

STATE_CANCEL = 0b001000
STATE_REJECT = 0b010000
STATE_VIOLATE = 0b100000

COMPLETE_BY_CANCEL = STATE_COMPLETE | STATE_CANCEL
COMPLETE_BY_REJECT = STATE_COMPLETE | STATE_REJECT
COMPLETE_BY_VIOLATE = STATE_COMPLETE | STATE_VIOLATE

import json

class _ATManager():
    def __init__(self, appID, appSecret):
        self.appID = appID
        self.appSecret = appSecret

    def _getAccessToken(self):
        rtn = {}

        url = ("http://api.weixin.qq.com/cgi-bin/token?grant_type="
                "client_credential&appid=%s&secret=%s" % (self.appID, self.appSecret))
        res = requests.get(url).json()
        if 'access_token' in res:
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

# from app.reservation.subscription import _ATManager

def sendRsvSubscMsg_Test():
    """
    Args:
        touserId: touser's openID
        rsv: the reservation object
    
    Returns:
        A json Object:
        { 
            "errcode":
            "errmsg:
        }
        API "https://api.weixin.qq.com/wxaapi/newtmpl/addtemplate?access_token=ACCESS_TOKEN" 's response
    """
    postData = {}

    postData['touser'] = OPEN_ID
    postData['template_id'] = SUBSC_TPL_ID
    postData['lang'] = "zh_CN"
    # postData['page'] = "pages/index/index"

    # rsverID = rsv.guest # 用户的openID
    # rsver = (
    #     db.session.query("user")
    #     .fliter(User.openid == rsverID)
    #     .first().name
    # )   # 用户的姓名
    rsver = "祝尔乐"
    
    # itemID = rsv.itemId
    # rsvItem = Item.queryItemName(itemId=itemID) # 预约物品名字
    rsvItem = "物品"

    rsvMeth = 0b11
    rsvMethod = []
    if rsvMeth & 0b01:
        rsvMethod.append("时间段预约")
    if rsvMeth & 0b10:
        rsvMethod.append("灵活预约")
    rsvMethod = ",".join(rsvMethod)    

    rsvStt = 0b100000
    rsvSttDict: dict[int, str] = {
        STATE_WAIT: "预约在等待审核",
        STATE_START: "预约已开始",
        STATE_COMPLETE: "预约已结束",
        STATE_CANCEL: "预约已取消",
        STATE_REJECT: "预约已被拒绝",
        STATE_VIOLATE: "预约出现违规",
        COMPLETE_BY_CANCEL: "预约被取消，已结束",
        COMPLETE_BY_VIOLATE: "预约出现违规，已结束",
        COMPLETE_BY_REJECT: "预约被拒绝，已结束"
    }
    rsvState = rsvSttDict[rsvStt]

    rsvReason = "想预约东西"
    
    postData['data'] = {
        "name1":{
            "value": rsver
        },  # 预约者姓名

        "thing13":{
            "value": rsvItem
        },  # 预约项目

        "thing28":{
            "value": rsvMethod
        },  # 预约类型

        "phrase14":{
            "value": rsvState
        },  # 预约状态

        "thing7":{
            "value": rsvReason
        }   # 预约备注
    }

    accessToken = _ATManager(WX_APP_ID, WX_APP_SECRET).getAccessToken()   # 获取accessToken
    # postData['access_token'] = accessToken
    print("get access token: %s" % accessToken)
    print('postData: \n' + str(postData))
    postData = json.dumps(postData)
    url = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=%s" % accessToken
    print("url:" + str(url))
    rqHeaders = {'Content-Type': 'application/json'}
    res = requests.post(url, headers=rqHeaders, data=postData)

    return res

def main():
    res = sendRsvSubscMsg_Test().json()
    print('errcode: ' + str(res['errcode']))
    print('errmsg: ' + str(res['errmsg']))

if __name__ == '__main__':
    main()