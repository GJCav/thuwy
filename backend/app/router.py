from flask import Blueprint, request, session
from flask_sqlalchemy import BaseQuery
import requests as R
import requests.exceptions as RE
import json as Json
import functools

from .models import *
from config import WX_APP_ID, WX_APP_SECRET

router = Blueprint('router', __name__)

@router.route('/login/', methods=['POST'])
def login():
    data: dict = request.get_json()
    if not data or not data.get('code', None):
        return {'code': 4, 'errmsg': 'request args missing'}

    try:
        res = R.get(f'https://api.weixin.qq.com/sns/jscode2session?'  \
            + f'appid={WX_APP_ID}&secret={WX_APP_SECRET}&'      \
            + f"js_code={data['code']}&grant_type=authorization_code", timeout=5)
    
        if res.status_code != 200:
            return {'code': 201, 'errmsg': 'not 200 response'}

        resJson: dict = Json.loads(res.text)
        if 'errcode' not in resJson \
            or 'openid' not in resJson \
            or not resJson['openid'] \
            or 'session_key' not in resJson \
            or not resJson['session_key']:

            return {'code': 202, 'errmsg': 'incomplete wx responce'}

        if resJson['errcode'] != 0:
            return {'code': 203, 'errmsg': 'wx reject svr', 'wx-code': resJson['errcode'], 'wx-errmsg': resJson.get('errmsg', '')}

        openid = str(resJson['openid'])
        session['wx-skey'] = str(resJson["session_key"])
        session['openid'] = openid
    except RE.Timeout:
        return {'code': 102, 'errmsg': 'svr request timeout'}
    except RE.ConnectionError as e:
        return {'code': 103, 'errmsg': 'svr cnt err'}
    except:
        return {'code': 200, 'errmsg': 'unknown error'}

    exist = db.session \
        .query(User.openid) \
        .filter_by(openid=openid) \
        .limit(1) \
        .count()

    
    if exist == 0:
        db.session.add(User(openid))
        db.session.commit()

    return {"code": 0, 'errmsg': 'success'}
    

def requireLogin(handler):
    @functools.wraps(handler)
    def inner(*args, **kwargs):
        if not session.get('openid', None):
            return {'code': 1, 'errmsg': 'not logged in'}
        else:
            return handler(*args, **kwargs)
    return inner

@router.route('/bind/', methods=['POST'])
@requireLogin
def bind():
    pass