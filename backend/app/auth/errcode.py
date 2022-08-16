CODE_LOGIN_NOT_200 = {"code": 201, "errmsg": "请求微信失败"}
CODE_LOGIN_INCOMPLETE_WX_RES = {"code": 202, "errmsg": "微信返回信息不完整"}
CODE_LOGIN_WEIXIN_REJECT = {
    "code": 203,
    "errmsg": "微信拒绝了服务器",
}  # , 'wx-code': resJson['errcode'], 'wx-errmsg': resJson.get('errmsg', '')}
CODE_LOGIN_TIMEOUT = {"code": 102, "errmsg": "请求微信超时"}
CODE_LOGIN_CNT_ERROR = {"code": 103, "errmsg": "链接微信失败"}
CODE_LOGIN_UNKOWN = {"code": 200, "errmsg": "未知错误，丢人gjm没有考虑这个情况"}

CODE_ALREADY_BOUND = {"code": 101, "errmsg": "请勿重复绑定"}
CODE_TARGET_BOUND = {"code": 102, "errmsg": "信息已被绑定"}
CODE_INVALID_BIND = {"code": 103, "errmsg": "绑定信息错误"}

CODE_ALREADY_ADMIN = {"code": 101, "errmsg": "已经是管理员"}
CODE_ALREADY_REQUESTED = {"code": 102, "errmsg": "请勿重复请求"}

CODE_USER_NOT_FOUND = {"code": 301, "errmsg": "用户不存在"}

CODE_GROUP_EXISTED = {"code": 401, "errmsg": "已存在同名组"}
CODE_GROUP_NOT_FOUND = {"code": 402, "errmsg": "找不到这个组"}
CODE_GROUP_MEMBER_EXISTED = {"code": 403, "errmsg": "用户已在该组中"}
CODE_GROUP_MEMBER_NOT_FOUND = {"code": 404, "errmsg": "组中找不到该用户"}

CODE_SCOPE_NOT_FOUND = {"code": 411, "errmsg": "不存在这个Scope"}

CODE_PRIVILEGE_EXISTED = {"code": 421, "errmsg": "用户已经具有这个权限"}
CODE_PRIVILEGE_NOT_FOUND = {"code": 422, "errmsg": "用户不具备指定权限"}