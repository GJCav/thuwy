CODE_TIME_CONFLICT = {"code": 101, "errmsg": "时间冲突"}
CODE_TIME_OUT_OF_RANGE = {"code": 102, "errmsg": "超出预约时限"}
CODE_DUPLICATE_METHOD = {"code": 103, "errmsg": "预约方法重复"}
CODE_METHOD_NOT_SUPPORT = {"code": 103, "errmsg": "预约方法不支持"}

CODE_RSV_NOT_FOUND = {"code": 101, "errmsg": "未找到该预约"}
CODE_RSV_START = {"code": 202, "errmsg": "预约已开始"}
CODE_RSV_COMPLETED = {"code": 203, "errmsg": "预约已结束"}
CODE_RSV_REJECTED = {"code": 204, "errmsg": "预约被拒绝"}
CODE_RSV_WAITING = {"code": 205, "errmsg": "预约等待审核"}

import app.item.errcode as __ItemErrCode

CODE_ITEM_NOT_FOUND = {
    "code": __ItemErrCode.CODE_ITEM_NOT_FOUND["code"] + 100,
    "errmsg": __ItemErrCode.CODE_ITEM_NOT_FOUND["errmsg"],
}