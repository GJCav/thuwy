CODE_SUCCESS = {"code": 0, "errmsg": "成功"}
CODE_NOT_LOGGED_IN = {"code": 1, "errmsg": "未登录"}
CODE_UNBOUND = {"code": 2, "errmsg": "未绑定"}
CODE_NOT_ADMIN = {"code": 3, "errmsg": "需要管理员权限"}
CODE_ARG_MISSING = {"code": 4, "errmsg": "参数缺失"}
CODE_ARG_FORMAT_ERR = {"code": 5, "errmsg": "参数格式错误"}
CODE_ARG_TYPE_ERR = {"code": 6, "errmsg": "参数类型错误"}
CODE_ARG_INVALID = {"code": 7, "errmsg": "参数非法"}
CODE_ACCESS_DENIED = {"code": 8, "errmsg": "您无此权限"}

CODE_DATABASE_ERROR = {"code": 20, "errmsg": "数据库错误"}
CODE_DATABASE_CONSISTANCE_ERROR = {"code": 21, "errmsg": "database consistance error"}

CODE_SERVER_BUGS = {"code": -100, "errmsg": "服务器错误"}

def wrap_database_error(e: Exception):
    rtn = {"exception": str(e)}
    rtn.update(CODE_DATABASE_ERROR)
    return rtn