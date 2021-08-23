import pytest
from testItemAPI import addItem
from config4test import R, baseUrl

import sys
sys.path.append('..')
import app.comerrs as ErrCode
import app.checkargs as CheckArgs
import app.timetools as T
from app.models import FlexTimeRsv
import app.rsvstate as RsvState


url_profile = baseUrl + 'profile/'
url_rsv = baseUrl + 'reservation/'

# ------------- pre test --------------

@pytest.mark.skip
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

@pytest.mark.skip
def testLoginAndBinding():
    global headers

    res = R.post(url_rsv, json={})
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
    itemIds.append(addItem(1, 1))
    itemIds.append(addItem(2, 2))
    itemIds.append(addItem(3, 3))
    itemIds.append(addItem(4, 0))

def _flexInterval(daysAfter: int, st, ed) -> str:
    st = T.clockAfter(T.daysAfter(daysAfter), *st)
    ed = T.clockAfter(T.daysAfter(daysAfter), *ed)
    # interval = f'{T.getDate(st)} {T.getHour(st)}:{T.getMins(st)}-{T.getHour(ed)}:{T.getMins(ed)}'
    interval = '{} {:0>2}:{:0>2}-{:0>2}:{:0>2}'.format(T.getDate(st), T.getHour(st), T.getMins(st), T.getHour(ed), T.getMins(ed))
    return interval

def testRsvFlexTime():
    if not itemIds:
        testPrepareItems()

    # -----------------  功能测试  ----------------------
    testData = [
        # (daysAfter, stHour, stMins, edHour, edMins, code, msg)
        (1,  8, 30, 14, 59,   0, '正常预约'),
        (1,  5,  0,  5, 30,   0, '正常预约'),
        (1,  6,  0,  8, 31, 101, '包含左端'),
        (1,  9,  0, 12,  0, 101, '被全包含'),
        (1, 13,  0, 15,  0, 101, '包含右端'),
        (1, 18,  0, 20,  0,   0, '正常预约'),
        (1,  8,  0, 15, 10, 101, '包含全段'),

        # 极限情况测试
        (1,  4, 30,  5,  0,   0, '重合右端，允许'),
        (1,  5,  0,  5,  1, 101, '重合左端，禁止'),
        (1,  5,  0,  5, 30, 101, '完全重合，禁止'), 
        
        # 再过一天
        (2,  8, 30, 14, 59,   0, '正常预约'),
        (2,  5,  0,  5, 30,   0, '正常预约'),
        (2, 18,  0, 20,  0,   0, '正常预约'),

        # 超过出预约范围
        (-1, 8,  0,  9, 10, 102, '预约昨天'),
        (8,  8,  0,  9, 10, 102, '预约一个星期之后的时间')
    ]

    for tId, data in enumerate(testData):
        days, stH, stM, edH, edM, code, msg = data

        interval = _flexInterval(days, (stH, stM), (edH, edM))
        itemId = itemIds[1]

        reqJson = {
            'item-id': itemId,
            'reason': f'test flex time rsv {tId}',
            'method': 2,
            'interval': interval
        }

        res = R.post(url_rsv, json=reqJson)
        assert res
        
        json = res.json()
        assert json['code'] == code, f"test: {msg}, get: {json['code']}, expect: {code}"

        if code != 0:
            continue

        rsvId = json['rsv-id']
        res = R.get(url_rsv + str(rsvId))
        assert res
        
        json = res.json()
        assert json['code'] == 0, (json, reqJson)

        rsv = json['rsv']
        assert CheckArgs.hasAttrs(rsv, ['id', 'item-id', 'guest', 'reason', 'method', 'state', 'interval', 'approver', 'exam-rst']), str(rsv)
        assert rsv['id'] == rsvId, str(rsv)
        assert rsv['item-id'] == itemId, str(rsv)
        assert rsv['reason'] == reqJson['reason'], rsv
        assert rsv['method'] == FlexTimeRsv.methodValue, str(rsv)
        assert rsv['state'] == RsvState.STATE_WAIT, rsv
        assert rsv['interval'] == interval

    reqJson = {
        'item-id': itemIds[0],
        'reason': f'test flex time rsv, rsv method not support',
        'method': 2,
        'interval': interval
    }
    res = R.post(url_rsv, json=reqJson)
    assert res
    json = res.json()
    assert json['code'] == ErrCode.Rsv.CODE_METHOD_NOT_SUPPORT['code'], f'测试方法不支持的情况: {json}'

    reqJson = {
        'item-id': 123,
        'reason': f'test flex time rsv, item not found',
        'method': 2,
        'interval': interval
    }
    res = R.post(url_rsv, json=reqJson)
    assert res
    json = res.json()
    assert json['code'] == ErrCode.Rsv.CODE_ITEM_NOT_FOUND['code'], f'测试找不到物品的情况: {json}'


    interval = _flexInterval(3, (8, 0), (9, 0))
    # ----------------------- 测试缺少参数的情况 ------------------------
    reqJson = {
        'item-id': itemIds[1],
        'reason': f'test flex time rsv, arg missing',
        'method': 2,
        'interval': interval
    }

    for k in reqJson.keys():
        mj = reqJson.copy()
        del mj[k]

        res = R.post(url_rsv, json=mj)
        assert res
        json = res.json()
        assert json['code'] == ErrCode.CODE_ARG_MISSING['code'], f'测试缺少参数的情况: {mj}'

    
    # --------------------- 测试参数类型错误的情况 ------------------------
    reqJson = {
        'item-id': itemIds[1],
        'reason': f'test flex time rsv, arg type error',
        'method': 2,
        'interval': interval
    }

    typeErrJson = {
        'item-id': 'abc',
        'reason': 125,
        'method': 1.5,
        'interval': ['nihao']
    }
    for k in typeErrJson.keys():
        temp = reqJson.copy()
        temp[k] = typeErrJson[k]

        res = R.post(url_rsv, json=temp)
        assert res
        json = res.json()
        assert json['code'] == ErrCode.CODE_ARG_TYPE_ERR['code'], f'测试参数类型错误的情况: {temp}'

    # ------------------- 测试参数格式错误的情况  -----------------------
    reqJson = {
        'item-id': itemIds[1],
        'reason': f'test flex time rsv, arg format error',
        'method': 2,
        'interval': interval
    }
    fmtErrJson = {
        'interval': 'abc'
    }
    for k in fmtErrJson.keys():
        temp = reqJson.copy()
        temp[k] = fmtErrJson[k]

        res = R.post(url_rsv, json=temp)
        assert res
        json = res.json()
        assert json['code'] == ErrCode.CODE_ARG_FORMAT_ERR['code'], f'测试参数格式错误的情况: {temp}\r\n{json}'
    
    # TODO: 等后端区分INVALID ERROR和FORMAT ERROR后添加INVALID的测试


def testRsvLongTime():
    if not itemIds:
        testPrepareItems()

    def _da(d):
        return T.getDate(T.daysAfter(d))

    testDataSet = [
        # code, interval
        (  0, [_da(1)+' 1']), # 单个预约
        (  0, [_da(1)+' 2']),
        (  0, [_da(1)+' 3']),

        (  0, [_da(2)+' 1', _da(2)+' 2']),  # 多个预约
        (  0, [_da(3)+' 2', _da(3)+' 3']),
        (  0, [_da(2)+' 3', _da(3)+' 1']),
        (  0, [_da(5)+' 1', _da(5)+' 2', _da(5)+' 3', _da(6)+' 2']),

        (101, [_da(1)+' 1']), # 时间冲突,
        (101, [_da(1)+' 2']),
        (101, [_da(1)+' 3']),
        (101, [_da(2)+' 1']),
        (101, [_da(2)+' 2']),
        (101, [_da(2)+' 3']),
        (101, [_da(3)+' 1']),
        (101, [_da(3)+' 2']),
        (101, [_da(3)+' 3']),
        (101, [_da(4)+' 1', _da(4)+' 1']), # 内部时间冲突
        (101, [_da(4)+' 2', _da(4)+' 2']),
        (101, [_da(4)+' 1', _da(4)+' 2', _da(4)+' 3', _da(4)+' 2']),

        (102, [_da(-1)+' 1']), # 超出预约范围
        (102, [_da(-1)+' 2']),
        (102, [_da(-1)+' 3']),
        (102, [_da(7)+' 1']),
        (102, [_da(7)+' 2']),
        (102, [_da(7)+' 3']),

        (  5, ['abcdeafccd 0']), # 日期格式错误
        (  5, [_da(5)]),
        (  5, ['225-asd5e cde e']),
        (  7, [_da(5)+' 6']),    # 时间码错误
    ]

    for idx, data in enumerate(testDataSet):
        expCode, interval = data
        reqJson = {
            'item-id': itemIds[0],
            'reason': f'test long time rsv, {idx}',
            'method': 1,
            'interval': interval
        }

        res = R.post(url_rsv, json=reqJson)
        assert res, data
        json = res.json()
        assert json['code'] == expCode, f"test: {data}, code: {json['code']}, exp: {expCode}"

        if expCode != 0: continue
        res = R.get(url_rsv+f"{json['rsv-id']}")
        assert res, f"test: {data}, recheck"
        json = res.json()
        assert json['code'] == 0
        rsv = json['rsv']
        assert rsv['interval'] == interval, f"test: {data}, recheck"


def _beforeSaturday():
    return T.getWDay(T.today()) < 6


@pytest.mark.skipif(not _beforeSaturday(), reason='no chance to reserve weekend now')
def testReserveWeekend():
    for i in range(7):
        if T.getWDay(T.daysAfter(i)) == 6:
            dateStr = T.getDate(T.daysAfter(i))

    itemId = addItem('test reserving weekend.', 3)

    sunday = T.getDate(T.daysAfter(1, T.parseDate(dateStr)))
    testDataSet = [
        (  0, [dateStr + ' 4']),
        (101, [dateStr + ' 1']),
        (101, [dateStr + ' 2']),
        (101, [dateStr + ' 3']),
        (101, [sunday + ' 1']),
        (101, [sunday + ' 2']),
        (101, [sunday + ' 3']),
        (  7, [sunday + ' 4'])
    ]

    for idx, data in enumerate(testDataSet):
        expCode, interval = data
        reqJson = {
            'item-id': itemId,
            'reason': f'test reserve weekend, {idx}',
            'method': 1,
            'interval': interval
        }

        res = R.post(url_rsv, json=reqJson)
        assert res, data
        json = res.json()
        assert json['code'] == expCode, f"test: {data}, code: {json['code']}, exp: {expCode}"

        if expCode != 0: continue
        res = R.get(url_rsv+f"{json['rsv-id']}")
        assert res, f"test: {data}, recheck"
        json = res.json()
        assert json['code'] == 0
        rsv = json['rsv']
        assert rsv['interval'] == interval, f"test: {data}, recheck"


def testExamRsv():
    itemId = addItem('test exam rsv, pass', 3)
    
    res = R.post(url_rsv, json={
        'item-id': itemId,
        'reason': 'test exam rsv, LongTimeRsv',
        'method': 1,
        'interval': [T.getDate(T.daysAfter(1)) + ' 1']
    })
    assert res, 'error at long time rsv'
    assert res.json()['code'] == 0, 'error at long time rsv'
    rsvId = res.json()['rsv-id']

    res = R.post(url_rsv + str(rsvId), json={
        'op': 1,
        'pass': 1,
        'reason': 'test pass'
    })
    assert res
    json = res.json()
    assert json['code'] == 0, json

    res = R.get(url_rsv+str(rsvId))
    assert res, 'recheck exam result'
    json = res.json()
    assert json['code'] == 0, json
    assert RsvState.isStart(json['rsv']['state']), json['rsv']

    # test reject
    itemId = addItem('test exam rsv, reject', 3)
    
    res = R.post(url_rsv, json={
        'item-id': itemId,
        'reason': 'test exam rsv, FlexRsv',
        'method': 2,
        'interval': _flexInterval(1, (14, 0), (16, 0))
    })
    assert res, 'error at flex time rsv'
    assert res.json()['code'] == 0, json
    rsvId = res.json()['rsv-id']

    res = R.post(url_rsv + str(rsvId), json={
        'op': 1,
        'pass': 0,
        'reason': 'test reject'
    })
    assert res
    json = res.json()
    assert json['code'] == 0, json

    res = R.get(url_rsv+str(rsvId))
    assert res, 'recheck exam result'
    json = res.json()
    assert json['code'] == 0, json
    assert RsvState.isReject(json['rsv']['state']) and RsvState.isComplete(json['rsv']['state']), json['rsv']




def testCancel():
    itemId = addItem('test cancel', 3)

    def _da(d):
        return T.getDate(T.daysAfter(d))
    
    # long time rsv
    reqJson = {
        'item-id': itemId,
        'reason': f'test cancel',
        'method': 1,
        'interval': [
            _da(1) + ' 1', _da(1) + ' 2', _da(1) + ' 3'
        ]
    }

    res = R.post(url_rsv, json=reqJson)
    assert res
    json = res.json()
    assert json['code'] == 0, json

    rsvId = json['rsv-id']

    res = R.delete(url_rsv+f'{rsvId}')
    assert res
    json = res.json()
    assert json['code'] == 0, json

    res = R.get(url_rsv+f'{rsvId}')
    assert res
    json = res.json()
    assert json['code'] == 0, json
    assert json['rsv']['state'] == RsvState.COMPLETE_BY_CANCEL, json

    res = R.delete(url_rsv+f'{rsvId}')
    assert res
    json = res.json()
    assert json['code'] == 203, json


