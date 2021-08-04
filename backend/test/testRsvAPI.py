# change this before test
cookieStr = \
"""session=eyJvcGVuaWQiOiJvZHo0QjR4bFRnbEJaWGpHSVZoNjVhRnNpeUFZIiwid3gtc2tleSI6Iis1aGxMcUlaZytzWWt0b3VUT3pJRGc9PSJ9.YQprBw.OuNPCemXItpUbTkougYvyBrnRO0; HttpOnly"""

import pytest
import requests as R
from testItemAPI import addItem

import sys
sys.path.append('..')
import app.comerrs as ErrCode
import app.checkargs as CheckArgs
import app.timetools as T
from app.models import FlexTimeRsv
import app.rsvstate as RsvState

url_server = 'http://127.0.0.1:5000/'
url_profile = url_server + 'profile/'
headers = {
    'cookie': cookieStr
}

url_rsv = url_server + 'reservation/'

# ------------- pre test --------------

def testRsvWithoutLogin():
    global url_rsv
    res = R.post(url_rsv, json={
        'item-id': 123,
        'reason': 'test',
        'method': 2,
        'interval': '2021-8-5 12:00-14:00'
    })

    assert res
    assert res.json()['code'] == ErrCode.CODE_NOT_LOGGED_IN['code']

def testLoginAndBinding():
    global headers

    res = R.post(url_rsv, headers=headers, json={})
    assert res

    reqJson = res.json()
    if reqJson['code'] == ErrCode.CODE_NOT_LOGGED_IN['code']:
        pytest.exit('not logged in')
    elif reqJson['code'] == ErrCode.CODE_UNBOUND['code']:
        pytest.exit("haven't bound.")

    assert reqJson['code'] == 0

# ---------- begin test -----------

itemIds = []

def testPrepareItems():
    itemIds.append(addItem(1, 1, headers))
    itemIds.append(addItem(2, 2, headers))
    itemIds.append(addItem(3, 3, headers))
    itemIds.append(addItem(4, 0, headers))

def _flexInterval(daysAfter: int, st, ed) -> str:
    st = T.clockAfter(T.daysAfter(daysAfter), *st)
    ed = T.clockAfter(T.daysAfter(daysAfter), *ed)
    interval = f'{T.getDate(st)} {T.getHour(st)}:{T.getMins(st)}-{T.getHour(ed)}:{T.getMins(ed)}'
    return interval

def testRsvFlexTime():
    if not itemIds:
        testPrepareItems()

    interval = _flexInterval(1, (8, 30), (14, 59))
    itemId = itemIds[1]

    reqJson = {
        'item-id': itemId,
        'reason': 'test flex time rsv',
        'method': 2,
        'interval': interval
    }

    res = R.post(url_rsv, headers=headers, json=reqJson)
    assert res
    
    json = res.json()
    assert json['code'] == 0, (json, reqJson)

    rsvId = json['rsv-id']
    res = R.get(url_rsv + str(rsvId))
    assert res
    
    json = res.json()
    assert json['code'] == 0, (json, reqJson)

    rsv = json['rsv']
    assert CheckArgs.hasAttrs(rsv, ['id', 'item-id', 'guest', 'reason', 'method', 'state', 'interval', 'approver', 'exam-rst']), str(rsv)
    assert rsv['id'] == rsvId, str(rsv)
    assert rsv['item-id'] == itemId, str(rsv)
    assert rsv['reason'] == 'test flex time rsv', str(rsv)
    assert rsv['method'] == FlexTimeRsv.methodValue, str(rsv)
    assert rsv['state'] == RsvState.STATE_WAITING
    assert rsv['interval'] == interval

# TODO: 添加FlexTimeRsv的更多测试