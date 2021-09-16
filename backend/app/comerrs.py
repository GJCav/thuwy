CODE_SUCCESS        = {'code': 0, 'errmsg': '成功'}
CODE_NOT_LOGGED_IN  = {'code': 1, 'errmsg': '未登录'}
CODE_UNBOUND        = {'code': 2, 'errmsg': '未绑定'}
CODE_NOT_ADMIN      = {'code': 3, 'errmsg': '需要管理员权限'}
CODE_ARG_MISSING    = {'code': 4, 'errmsg': '参数缺失'}
CODE_ARG_FORMAT_ERR = {'code': 5, 'errmsg': '参数格式错误'}
CODE_ARG_TYPE_ERR   = {'code': 6, 'errmsg': '参数类型错误'}
CODE_ARG_INVALID    = {'code': 7, 'errmsg': '参数非法'}

CODE_DATABASE_ERROR = {'code': 20, 'errmsg': '数据库错误'}

CODE_SERVER_BUGS = {'code': -100, 'errmsg': '服务器错误'}

class Auth:
   CODE_LOGIN_NOT_200 = {'code': 201, 'errmsg': '请求微信失败'}
   CODE_LOGIN_INCOMPLETE_WX_RES = {'code': 202, 'errmsg': '微信返回信息不完整'}
   CODE_LOGIN_WEIXIN_REJECT = {'code': 203, 'errmsg': '微信拒绝了服务器' } # , 'wx-code': resJson['errcode'], 'wx-errmsg': resJson.get('errmsg', '')}
   CODE_LOGIN_TIMEOUT = {'code': 102, 'errmsg': '请求微信超时'}
   CODE_LOGIN_CNT_ERROR = {'code': 103, 'errmsg': '链接微信失败'}
   CODE_LOGIN_UNKOWN = {'code': 200, 'errmsg': '未知错误，丢人gjm没有考虑这个情况'}

   CODE_ALREADY_BOUND = {'code': 101,'errmsg': '请勿重复绑定'}
   CODE_TARGET_BOUND = {'code': 102,'errmsg': '信息已被绑定'}
   CODE_INVALID_BIND = {'code': 103, 'errmsg': '绑定信息错误'}

   CODE_ALREADY_ADMIN = {'code': 101, 'errmsg': '已经是管理员'}
   CODE_ALREADY_REQUESTED = {'code': 102, 'errmsg': '请勿重复请求'}

   CODE_USER_NOT_FOUND = {'code': 301, 'errmsg': '用户不存在'}

class Item:
   CODE_ITEM_NOT_FOUND = {'code': 101, 'errmsg': '未找到物品'}


class Rsv:
   CODE_TIME_CONFLICT      = {'code': 101, 'errmsg': '时间冲突'}
   CODE_TIME_OUT_OF_RANGE  = {'code': 102, 'errmsg': '超出预约时限'}
   CODE_DUPLICATE_METHOD   = {'code': 103, 'errmsg': '预约方法重复'}
   CODE_METHOD_NOT_SUPPORT = {'code': 103, 'errmsg': '预约方法不支持'}

   CODE_RSV_NOT_FOUND = {'code': 101, 'errmsg': '未找到该预约'}
   CODE_RSV_START     = {'code': 202, 'errmsg': '预约已开始'}
   CODE_RSV_COMPLETED = {'code': 203, 'errmsg': '预约已结束'}
   CODE_RSV_REJECTED  = {'code': 204, 'errmsg': '预约被拒绝'}
   CODE_RSV_WAITING   = {'code': 205, 'errmsg': '预约等待审核'}

   CODE_ITEM_NOT_FOUND = {
      'code': Item.CODE_ITEM_NOT_FOUND['code']+100,
      'errmsg': Item.CODE_ITEM_NOT_FOUND['errmsg']
   }

class Advice:
   CODE_ADVICE_NOT_FOUND = {'code': 101, 'errmsg': '未找到该反馈'}


class Carousel:
   CODE_MSG_NOT_FOUND = {'code': 101, 'errmsg': '未找到该宣传'}