CODE_SUCCESS        = {'code': 0, 'errmsg': 'success'}
CODE_NOT_LOGGED_IN  = {'code': 1, 'errmsg': 'not logged in'}
CODE_UNBOUND        = {'code': 2, 'errmsg': 'unbound'}
CODE_NOT_ADMIN      = {'code': 3, 'errmsg': 'not admin'}
CODE_ARG_MISSING    = {'code': 4, 'errmsg': 'request args missing'}
CODE_ARG_FORMAT_ERR = {'code': 5, 'errmsg': 'request args format error'}
CODE_ARG_TYPE_ERR   = {'code': 6, 'errmsg': 'request args type error'}
CODE_ARG_INVALID    = {'code': 7, 'errmsg': 'request args are invalid'}

CODE_DATABASE_ERROR = {'code': 20, 'errmsg': 'database error'}

class Item:
   CODE_ITEM_NOT_FOUND = {'code': 101, 'errmsg': 'item not found'}


class Rsv:
   CODE_TIME_CONFLICT = {'code': 101, 'errmsg': 'time conflict'}
   CODE_TIME_OUT_OF_RANGE = {'code': 102, 'errmsg': 'reservation time out of range'}
   CODE_DUPLICATE_METHOD = {'code': 103, 'errmsg': 'using duplicated method'}
   CODE_METHOD_NOT_SUPPORT = {'code': 103, 'errmsg': 'rsv method not supported yet'}

   CODE_ITEM_NOT_FOUND = {
      'code': Item.CODE_ITEM_NOT_FOUND['code']+100,
      'errmsg': Item.CODE_ITEM_NOT_FOUND['errmsg']
   }