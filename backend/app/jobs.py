import traceback

from . import scheduler, app, db
from .models import Item, Reservation, LongTimeRsv
from . import timetools as timestamp
from . import rsvstate as RsvState

from config import userSysName

@scheduler.task('cron', minute='*', hour='8-23,3')
def autoReject():
    with app.app_context():
        qryRst = db.session.query(Reservation)\
            .filter(Reservation.st <= timestamp.now())\
            .filter(Reservation.state == RsvState.STATE_WAIT)\
            .all()
        
        for rsv in qryRst:
            if rsv.method == LongTimeRsv.methodValue\
                and LongTimeRsv.isChildRsv(rsv):
                continue

            # print(f'auto reject: {rsv.id}')
            rsv.examRst = '预约到达开始时间仍未审核，系统自动拒绝'
            rsv.approver = userSysName
            rsv.changeState(RsvState.COMPLETE_BY_REJECT)
        
        try:
            db.session.commit()
        except Exception as e:
            traceback.print_exc()

@scheduler.task('cron', minute='*', hour='8-23,3')
def autoComplete():
    with app.app_context():
        autoCompleteQryRst = db.session.query(Item.id).filter(Item.attr.op('&')(1)).all()
        for row in autoCompleteQryRst:
            itemId = row[0]
            qryRst = db.session.query(Reservation)\
                .filter(Reservation.itemId == itemId)\
                .filter(Reservation.state.op('&')(RsvState.STATE_START))\
                .filter(Reservation.ed < timestamp.now())\
                .all()
            
            for rsv in qryRst:
                if LongTimeRsv.isChildRsv(rsv):
                    continue

                if rsv.getEndTime() >= timestamp.now(): # LongTimeRsv 的一部分结束了，但另一部分还没结束
                    continue

                rsv.changeState(RsvState.STATE_COMPLETE)

        try:
            db.session.commit()
        except:
            traceback.print_exc()

            