from flask import request, session

from . import adviceRouter
from app.auth import requireAdmin, requireBinding, requireLogin
from app.models import Advice
from app import comerrs as ErrCode
from app import adviceIdPool, db
from app import timetools as timestamp
from app import checkargs as CheckArgs
from app import snowflake

@adviceRouter.route('/advice/')
@requireLogin
@requireBinding
@requireAdmin
def getAdviceList():
    st = request.args.get('st', None)
    ed = request.args.get('ed', None)
    state = request.args.get('state', None, int)
    page = request.args.get('p', None)

    try:
        page = int(page)
    except:
        return ErrCode.CODE_ARG_TYPE_ERR
    
    if not CheckArgs.isUint64(page) or page <= 0:
        return ErrCode.CODE_ARG_INVALID


    qry = db.session.query(Advice)
    
    if st != None:
        try:
            st = timestamp.parseDate(st)
        except Exception as e:
            return ErrCode.CODE_ARG_FORMAT_ERR
        qry = qry.filter(Advice.id >= snowflake.makeId(st, 0, 0))
    
    if ed != None:
        try:
            ed = timestamp.parseDate(ed)
        except Exception as e:
            return ErrCode.CODE_ARG_FORMAT_ERR
        qry = qry.filter(Advice.id < snowflake.makeId(ed, 0, 0))
    
    if state != None:
        qry = qry.filter(Advice.state == state)

    qryRst = qry.limit(20).offset(20*(page-1)).all()

    rtn = {}
    rtn.update(ErrCode.CODE_SUCCESS)
    rtn['page'] = page
    rtn['advice'] = []
    for advice in qryRst:
        rtn['advice'].append(advice.toDict())
    return rtn

@adviceRouter.route('/advice/<int:adviceId>/')
@requireLogin
@requireBinding
@requireAdmin
def getAdviceInfo(adviceId):
    if not CheckArgs.isUint64(adviceId):
        return ErrCode.CODE_ARG_INVALID

    advice = Advice.queryById(adviceId)

    if not advice:
        return ErrCode.Advice.CODE_ADVICE_NOT_FOUND

    rtn = {}
    rtn.update(ErrCode.CODE_SUCCESS)
    rtn['advice'] = advice.toDict(True)
    return rtn

@adviceRouter.route('/advice/<int:adviceId>/', methods=['POST'])
@requireLogin
@requireBinding
@requireAdmin
def responseAdvice(adviceId):
    if not CheckArgs.isUint64(adviceId):
        return ErrCode.CODE_ARG_INVALID

    json = request.get_json()
    if json == None:
        return ErrCode.CODE_ARG_INVALID
    if 'response' not in json:
        return ErrCode.CODE_ARG_MISSING
    if not CheckArgs.isStr(json['response']):
        return ErrCode.CODE_ARG_TYPE_ERR

    advice = Advice.queryById(adviceId)

    if not advice:
        return ErrCode.Advice.CODE_ADVICE_NOT_FOUND

    advice.response = json['response']
    advice.state = Advice.STATE_END

    try:
        db.session.commit()
    except Exception as e:
        print(str(e))
        return ErrCode.CODE_DATABASE_ERROR

    return ErrCode.CODE_SUCCESS

@adviceRouter.route('/advice/', methods=['POST'])
@requireLogin
@requireBinding
def adminAdvice():
    json = request.get_json()

    if not json: return ErrCode.CODE_ARG_INVALID
    if not CheckArgs.hasAttrs(json, ['title', 'content']):
        return ErrCode.CODE_ARG_MISSING
    if not CheckArgs.areStr(json, ['title', 'content']):
        return ErrCode.CODE_ARG_TYPE_ERR
    
    advice = Advice()
    advice.id = adviceIdPool.next()
    advice.proponent = session['openid']
    advice.title = json['title']
    advice.content = json['content']
    advice.state = Advice.STATE_WAIT
    
    db.session.add(advice)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return ErrCode.CODE_DATABASE_ERROR

    rtn = {}
    rtn.update(ErrCode.CODE_SUCCESS)
    rtn['advice-id'] = advice.id
    return rtn