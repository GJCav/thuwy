from flask import request
import json as Json

from . import itemRouter

from app import db, itemIdPool
from app import comerrs as ErrCode
from app.models import Admin, AdminRequest, LongTimeRsv, User, Item, Reservation
import app.checkargs as CheckArgs
from app.auth import requireAdmin, requireBinding, requireLogin
import app.timetools as timestamp

@itemRouter.route('/item/', methods=['GET'])
def itemlist():
    page = request.args.get('p', '1')
    try:
        page = int(page)
    except:
        return ErrCode.CODE_ARG_TYPE_ERR
    
    page -= 1
    if page >= (1<<65)-1 or page < 0:
        return ErrCode.CODE_ARG_INVALID
    
    itemCount = db.session.query(Item.id).filter(Item.delete == 0).count()
    items = Item.query.filter(Item.delete == 0).limit(20).offset(20*page).all()
    items = [e.toDict() for e in items]

    # pprint(items)

    rst = ErrCode.CODE_SUCCESS.copy()
    rst.update({
        'item-count': itemCount,
        'page': page+1,
        'items': items
    })

    return rst


@itemRouter.route('/item/<int:itemId>', methods=['GET'])
def itemInfo(itemId):

    if not CheckArgs.isUint64(itemId):
        return ErrCode.CODE_ARG_INVALID
    
    item = db.session.query(Item).filter(Item.id == itemId).one_or_none()
    if not item:
        return ErrCode.Item.CODE_ITEM_NOT_FOUND
    else:
        rst = {}
        rst.update(ErrCode.CODE_SUCCESS)
        rst['item'] = item.toDict()
        rst['item']['md-intro'] = item.mdIntro
        rst['item']['delete'] = item.delete
        return rst

@itemRouter.route('/item/', methods=['POST'])
@requireLogin
@requireBinding
@requireAdmin
def addItem():
    reqJson = request.json

    if not reqJson.get('name') \
        or not reqJson.get('brief-intro') \
        or not reqJson.get('md-intro') \
        or not reqJson.get('thumbnail') \
        or reqJson.get('rsv-method') == None:

        # pprint(reqJson)
        return ErrCode.CODE_ARG_MISSING

    if not CheckArgs.areStr(reqJson, ['name', 'brief-intro', 'md-intro', 'thumbnail']) \
        or not CheckArgs.areInt(reqJson, ['rsv-method']):
        # pprint(reqJson)
        return ErrCode.CODE_ARG_TYPE_ERR

    try:
        item            = Item()
        item.id         = itemIdPool.next()
        item.name       = reqJson['name']
        item.available  = True
        item.delete     = False
        item.rsvMethod  = int(reqJson['rsv-method'])
        item.briefIntro = reqJson['brief-intro']

        if not CheckArgs.isUrl(reqJson['thumbnail']): # TODO: 这里可以进一步限制
            return ErrCode.CODE_ARG_FORMAT_ERR
        item.thumbnail  = reqJson['thumbnail']
        item.mdIntro    = reqJson['md-intro']
    except:
        return ErrCode.CODE_ARG_TYPE_ERR

    try:
        db.session.add(item)
        db.session.commit()
    except:
        db.session.rollback()
        return ErrCode.CODE_DATABASE_ERROR
    rtn = {}
    rtn.update(ErrCode.CODE_SUCCESS)
    rtn['item-id'] = item.id
    return rtn


@itemRouter.route('/item/<int:itemId>', methods=['POST'])
@requireLogin
@requireBinding
@requireAdmin
def modifyItem(itemId):
    item = db.session.query(Item).filter(Item.id == itemId).one_or_none()
    if not item: return ErrCode.Item.CODE_ITEM_NOT_FOUND

    itemJson = request.json

    try:
        if 'name' in itemJson: item.name              = str(itemJson['name'])
        if 'available' in itemJson: item.available    = bool(itemJson['available'])
        if 'rsv-method' in itemJson: item.rsvMethod   = int(itemJson['rsv-method'])
        if 'brief-intro' in itemJson: item.briefIntro = itemJson['brief-intro']
        if 'thumbnail' in itemJson: item.thumbnail    = itemJson['thumbnail']
        if 'md-intro' in itemJson: item.mdIntro       = itemJson['md-intro']
    except:
        return ErrCode.CODE_ARG_TYPE_ERR
    
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return ErrCode.CODE_DATABASE_ERROR

    return ErrCode.CODE_SUCCESS


@itemRouter.route('/item/<int:itemId>', methods=['DELETE'])
@requireLogin
@requireBinding
@requireAdmin
def delItem(itemId):
    if not CheckArgs.isUint64(itemId): return ErrCode.CODE_ARG_INVALID
    item = db.session.query(Item).filter(Item.id == itemId).one_or_none() 
    if not item: return ErrCode.Item.CODE_ITEM_NOT_FOUND

    try:
        item.delete = True
        db.session.commit()
    except:
        db.session.rollback()
        return ErrCode.CODE_DATABASE_ERROR
    
    return ErrCode.CODE_SUCCESS


@itemRouter.route('/item/<int:itemId>/reservation')
def itemRsvInfo(itemId):
    qryRst = \
        db.session.query(Reservation) \
        .filter(Reservation.itemId == itemId) \
        .filter(Reservation.st >= timestamp.today()) \
        .filter(Reservation.ed <= timestamp.aWeekAfter()) \
        .all()

    skipRsvIds = set()
    arr = []
    for rsv in qryRst:
        if rsv.id in skipRsvIds:
            continue

        if LongTimeRsv.isChildRsv(rsv):
            rsv = LongTimeRsv.getFatherRsv(rsv)
            
        if LongTimeRsv.isFatherRsv(rsv):
            choreJson = Json.loads(rsv.chore)
            skipRsvIds |= set(choreJson['group-rsv']['sub-rsvs'])
            skipRsvIds.add(rsv.id)

        arr.append(rsv.toDict())

    rst = {}
    rst.update(ErrCode.CODE_SUCCESS)
    def _process(e):
        del e['item-id']
        del e['guest']
        del e['reason']
        del e['approver']
        del e['exam-rst']
        return e

    rst['rsvs'] = [_process(e) for e in arr] # 因为字段名和协议中属性名相同，所以不用多处理
    return rst
