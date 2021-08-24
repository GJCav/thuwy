from . import scheduler, app, db
from .models import Reservation, LongTimeRsv
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
            print(e)