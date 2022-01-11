
from flask_sqlalchemy import SQLAlchemy
from config import userSysName

db = SQLAlchemy(use_native_unicode='utf8')


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
        from app.auth import init_sys_account
        init_sys_account()
    pass

# 太TM神奇了，python的dict没有__dict__属性，不能动态添加属性，如：
#   a = {}
#   a.foo = 10 # 报错：AttributeError
# 此时setattr也没用，因为dict重写了__setattr__
# 但自己写的类默认是有__dict__的，也就是可以setattr
# 如果自己写的类有__slot__，那么也不能动态添加，sqlachemy.engine.row.Row 就这么干的

class _Dict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    def __getattribute__(self, name: str):
        if name in self: return self[name]
        else: return super().__getattribute__(name)

    def __setattr__(self, name: str, value) -> None:
        self[name] = value

# """
# 即使是LongTimeRsv，也只返回单挑 interval 
# """
# def _getIntervalStr(self: Reservation):
#     """
#     self中至少有Reservation中的如下属性：
#         * method
#         * st
#         * ed
#     return: 可读的时间段信息
#     """
#     if self.method == LongTimeRsv.methodValue:
#         hour = timestamp.getHour(self.st)
#         if hour == LongTimeRsv.morningStartHour:
#             return f'{timestamp.getDate(self.st)} {LongTimeRsv.morningCode}'
#         elif hour == LongTimeRsv.afternoonStartHour:
#             return f'{timestamp.getDate(self.st)} {LongTimeRsv.afternoonCode}'
#         elif hour == LongTimeRsv.nightStartHour:
#             return f'{timestamp.getDate(self.st)} {LongTimeRsv.nightCode}'
#         else:
#             return f'{timestamp.getDate(self.st)} {LongTimeRsv.weekendCode}'

#     elif self.method == FlexTimeRsv.methodValue:
#         return f'{timestamp.getDate(self.st)} {timestamp.clock(self.st)}-{timestamp.clock(self.ed)}'


# TODO: 换个更恰当的名字
# 20210823 有bug，而且非常丑陋，现在弃用
# def mergeAndBeautify(qryRst: list):
    # """
    # qryRst中的rsv对象至少包含如下属性：
    #     * id
    #     * method
    #     * st
    #     * ed
    #     * chore
    # """
    # groups = {}
    # rsvArr = []
    # for e in qryRst:
    #     # e: Row,
    #     # setattr(e, 'interval', None), 因为 e 是Row类型，不能动态添加属性，所以hack一下
    #     e = _Dict(**dict(e))
    #     e.interval = None

    #     if e.method == FlexTimeRsv.methodValue:
    #         e.interval = _getIntervalStr(e)
    #         rsvArr.append(e)
        
    #     elif e.method == LongTimeRsv.methodValue:
    #         relation: dict = Json.loads(e.chore)['group-rsv']
    #         if 'sub-rsvs' in relation:
    #             e.interval = []
    #             e.interval.append(_getIntervalStr(e))

    #             for subRsvIds in relation['sub-rsvs']:
    #                 if subRsvIds in groups:
    #                     e.interval.append(_getIntervalStr(groups[subRsvIds]))
                
    #             groups[e.id] = e
    #             rsvArr.append(e)
    #         else:
    #             if relation['fth-rsv'] in groups:
    #                 groups[relation['fth-rsv']].interval.append(_getIntervalStr(e))
    #             else:
    #                 groups[e.id] = e
    # return rsvArr