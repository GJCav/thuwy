import pytest
# import requests as R
import os.path as Path
import os
import math
from pprint import pprint
from copy import deepcopy
from random import randint
import sys

from config4test import R

sys.path.append('..')
import app.comerrs as ErrCode
import app.checkargs as CheckArgs

testItemCount = 100

addNewItem = True
testItemUrl = 'http://weiyang.grw20.cn:9090/item/'

# 在使用该测试前删除原来的数据库
@pytest.mark.skipif(addNewItem == False, reason='no need to add item')
@pytest.mark.addItem
def testAddItem():
    global testItemCount, testItemCount
    count = testItemCount
    url = testItemUrl

    print(f'test add {count} items...')
    for i in range(count):
        json = {
            'name': f'Item {i}',
            'brief-intro': f'bf-intro {i}',
            'md-intro': f'md {i}',
            'thumbnail': f'http://server/thumb{i}',
            'rsv-method': i % 2
        }
        res = R.post(url, json=json)
        assert res.status_code == 200
        assert res.json().get('code') == 0

    print(f'test verify items...')
    res = R.get(url)
    assert res.status_code == 200
    assert res.json()

    json: dict = res.json()
    assert json['code'] == 0
    assert json['item-count'] == count
    assert json['page'] == 1

    for i in range(1, math.ceil(count / 20) + 1):
        res = R.get(url+f'?p={i}')
        assert res.status_code == 200
        assert res.json()

        json: dict = res.json()
        assert json['code'] == 0
        assert json['item-count'] == count
        assert json['page'] == i

        for j in range(20):
            item = json['items'][j]
            idx = j + (i-1)*20
            assert item['name'] == f'Item {idx}'
            assert 'id' in item
            assert item['brief-intro'] == f'bf-intro {idx}'
            assert item['thumbnail'] == f'http://server/thumb{idx}'
            assert item['rsv-method'] == idx % 2

@pytest.mark.addItem
def testAddDuItem():
    global testItemUrl
    url = testItemUrl
    json = {
        'name': f'Item 0',
        'brief-intro': f'bf-intro 0',
        'md-intro': f'md 0',
        'thumbnail': f'http://server/thumb0',
        'rsv-method': 0
    }
    res = R.post(url=url, json = json)
    assert res.status_code == 200
    assert res.json()

    rtn: dict = res.json()
    assert rtn['code'] == 0  # duplicate item is allowed.


@pytest.mark.addItem
def testAddItemWithBadArg():
    global testItemUrl
    url = testItemUrl
    json = {
        'name': f'Item 0',
        'brief-intro': f'bf-intro 0',
        'md-intro': f'md 0',
        'thumbnail': f'http://server/thumb0',
        'rsv-method': 0
    }

    print('missing args')
    for k in json.keys():
        missArg = deepcopy(json)
        del missArg[k]
        res = R.post(url=url, json=missArg)
        
        assert res.status_code == 200
        resJson = res.json()
        assert resJson['code'] == 4
        assert resJson.keys() == {'code', 'errmsg'}

    for k in json.keys():
        missArg = deepcopy(json)
        missArg[k] = None
        res = R.post(url=url, json=missArg)
        
        assert res.status_code == 200
        resJson = res.json()
        assert resJson['code'] == 4
        assert resJson.keys() == {'code', 'errmsg'}

    print('wrong type args')
    for k in ['name', 'brief-intro', 'md-intro', 'thumbnail']:
        wtArg = deepcopy(json)
        wtArg[k] = 123
        res = R.post(url=url, json=wtArg)
        
        assert res.status_code == 200
        resJson = res.json()
        assert resJson['code'] == ErrCode.CODE_ARG_TYPE_ERR['code']
        assert resJson.keys() == {'code', 'errmsg'}

    for k in ['rsv-method']:
        wtArg = deepcopy(json)
        wtArg[k] = 'asdfasdf'
        res = R.post(url=url, json=wtArg)
        
        assert res.status_code == 200
        resJson = res.json()
        assert resJson['code'] == ErrCode.CODE_ARG_TYPE_ERR['code']
        assert resJson.keys() == {'code', 'errmsg'}

    print('wrong format args')
    for k in ['thumbnail']:
        wfArg = deepcopy(json)
        wfArg[k] = '------------'
        # pprint(wfArg)
        res = R.post(url=url, json=wfArg)
        
        assert res.status_code == 200
        resJson = res.json()
        assert resJson['code'] == ErrCode.CODE_ARG_FORMAT_ERR['code']
        assert resJson.keys() == {'code', 'errmsg'}

def _isItemObject(item: dict):
    # pprint(item.keys())
    assert item.keys() == {'name', 'id', 'available', 'brief-intro', 'thumbnail', 'rsv-method'}
    assert CheckArgs.areStr(item, ['name', 'brief-intro', 'thumbnail'])
    assert CheckArgs.isUrl(item['thumbnail'])
    assert CheckArgs.areInt(item, ['id', 'rsv-method'])
    assert CheckArgs.areBool(item, ['available'])

@pytest.mark.showItem
def testShowItem():
    global testItemUrl
    url = testItemUrl

    res = R.get(url)
    json: dict = res.json()
    assert json['code'] == 0
    # pprint(json.keys())
    assert CheckArgs.hasAttrs(json, ['code', 'errmsg', 'item-count', 'page', 'items'])
    assert CheckArgs.areInt(json, ['item-count', 'page'])
    assert json['page'] == 1

    maxPage = math.ceil(json['item-count'] / 20)
    for i in range(maxPage):
        res = R.get(url)
        json: dict = res.json()
        assert json['code'] == 0
        assert CheckArgs.hasAttrs(json, ['code', 'errmsg', 'item-count', 'page', 'items'])
        assert CheckArgs.areInt(json, ['item-count', 'page'])

        for item in json['items']:
           _isItemObject(item)

    res = R.get(f'{url}?p={maxPage+1}')
    assert res.status_code == 200
    assert len(res.json()['items']) == 0

    res = R.get(f'{url}?p={2**128}')
    assert res.json()['code'] == ErrCode.CODE_ARG_INVALID['code']

    res = R.get(f'{url}?p=0')
    assert res.json()['code'] == ErrCode.CODE_ARG_INVALID['code']


@pytest.mark.modifyItem
def testModifyItem():
    global testItemUrl
    url = testItemUrl

    res = R.get(url)
    json: dict = res.json()

    totPage = math.ceil(json['item-count'] / 20)
    page = randint(1, totPage)

    res = R.get(url+f'?p={page}')
    json: dict = res.json()
    idx = randint(0, len(json['items'])-1)
    oldItem = json['items'][idx]
    itemId = json['items'][idx]['id']

    mdf = {
        'name': f'name after modify p={page}, i={idx}',
        'available': 0,
        'brief-intro': f'b-i after modify p={page}, i={idx}',
        'md-intro': f'md-i after modify p={page}, i={idx}',
        'thumbnail': f'http://after modify p={page}, i={idx}',
        'rsv-method': 10
    }

    for k in mdf:
        if k == 'md-intro': continue

        reqJson = {k:mdf[k]}
        res = R.post(url+f'{itemId}', json=reqJson)
        assert res.status_code == 200
        json: dict = res.json()
        assert json.keys() == {'code', 'errmsg'}
        assert json['code'] == 0

        res = R.get(url+f'?p={page}')
        assert res.status_code == 200
        json: dict = res.json()


        oldItem.update({k: mdf[k]})
        assert oldItem == json['items'][idx], oldItem

    # TODO: test md-intro here


# TODO: testModifyItemWithBadArg

@pytest.mark.delItem
def testDelItem():
    global testItemUrl
    url = testItemUrl

    res = R.delete(url+'0')
    assert res
    assert res.json()['code'] == 101, '删除一个不存在的id'

    res = R.delete(url+'-1')
    assert res.status_code == 404, 'flask 不允许负数的url变量'

    res = R.delete(url+f'{2**128}')
    assert res
    assert res.json()['code'] == ErrCode.CODE_ARG_INVALID['code'], '测试一个过大id'

    res = R.delete(url+'12233')
    assert res
    assert res.json()['code'] == ErrCode.Item.CODE_ITEM_NOT_FOUND['code'], '测试不存在的id'

    json = R.get(url).json()
    while json['items']:
        for item in json['items']:
            itemId = item['id']
            res = R.delete(url+f'{itemId}')
            assert res
            assert res.json()['code'] == 0, f'删除物品: {item["name"]}, {item["id"]}'
        json = R.get(url).json()
    
    assert json['item-count'] == 0


# ------------ 给其他模块使用的函数 --------------
def addItem(i, rsvMethod):
    global testItemUrl
    url = testItemUrl
    json = {
        'name': f'Item {i}',
        'brief-intro': f'bf-intro {i}',
        'md-intro': f'md {i}',
        'thumbnail': f'http://server/thumb{i}',
        'rsv-method': rsvMethod
    }

    res = R.post(url, json=json)
    assert res, f"{res.reason} "
    
    json = res.json()
    assert json['code'] == 0, json
    return json['item-id']