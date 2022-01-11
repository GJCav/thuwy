
from config4test import R, baseUrl, headers
import requests
import pytest
import re as Regex

import sys
sys.path.append('..')
from app.comerrs import *
from app.advice.errcode import *

adviceUrl = baseUrl + 'advice/'

adviceIds = []

@pytest.mark.funcTest
def testAddAdvice():
    adviceCount = 10
    for i in range(adviceCount):
        reqJson = {
            'title': f'add advice {i}',
            'content': f'test add advice'
        }
        res = R.post(adviceUrl, json=reqJson)
        assert res
        json = res.json()
        assert json['code'] == 0, json

        adviceIds.append(json['advice-id'])

@pytest.mark.funcTest
def testGetAdviceList():
    page = 0
    idSet = set(adviceIds)
    while True:
        page += 1
        res = R.get(adviceUrl + f'?p={page}')
        assert res
        json = res.json()
        assert json['code'] == 0, json
        assert json['page'] == page, json
        assert 'advice' in json, json
        assert isinstance(json['advice'], list), json
        adviceArr = json['advice']

        if len(adviceArr) == 0:
            break
        
        curIdSet = set()
        for advice in adviceArr:
            advice: dict
            assert set(advice.keys()) == {'id', 'proponent', 'title', 'state', 'response'}
            curIdSet.add(advice['id'])

        idSet -= curIdSet

    assert len(idSet) == 0, f'建议列表没有完整显示添加的advice，未找到：{idSet}'

@pytest.mark.funcTest
def testGetAdviceInfo():
    for id in adviceIds:
        res = R.get(adviceUrl + f'{id}/')
        assert res
        json = res.json()
        assert json['code'] == 0, json
        advice: dict = json['advice']

        assert advice['id'] == id
        assert advice['proponent']
        assert Regex.match(r'add advice \d+', advice['title'])
        assert advice['content'] == 'test add advice'
        assert advice['state'] == 1, 'should be waiting state'
        assert advice['response'] == None

@pytest.mark.funcTest
def testResponse():
    for id in adviceIds:
        res = R.get(adviceUrl+ f'{id}/')
        assert res
        json = res.json()
        assert json['code'] == 0, json
        
        oldAdvice: dict = json['advice']

        reqJson = {
            'response': f'response {id}'
        }
        res = R.post(adviceUrl+f'{id}/', json=reqJson)
        assert res
        json = res.json()
        assert json['code'] == 0, json

        res = R.get(adviceUrl + f'{id}/')
        assert res
        json = res.json()
        assert json['code'] == 0, json
        advice: dict = json['advice']

        assert oldAdvice.keys() == advice.keys()
        assert oldAdvice['id'] == advice['id']
        assert oldAdvice['title'] == advice['title']
        assert oldAdvice['content'] == advice['content']
        assert advice['state'] == 2
        assert advice['response'] == f'response {id}'

@pytest.mark.robustTest
def testAddAdviceRobustly():
    baseReqJson = {
        'title': f'test add advice robustly',
        'content': f'test add advice'
    }

    for k in baseReqJson.keys():
        reqJson = {}
        reqJson.update(baseReqJson)
        del reqJson[k]

        res = R.post(adviceUrl, json=reqJson)
        assert res
        json = res.json()
        assert json['code'] == CODE_ARG_MISSING['code'], json

    for k in baseReqJson.keys():
        reqjson = {}
        reqJson.update(baseReqJson)
        reqJson[k] = 10

        res = R.post(adviceUrl, json=reqJson)
        assert res
        json = res.json()
        assert json['code'] == CODE_ARG_TYPE_ERR['code'], json

@pytest.mark.robustTest
def testGetAdviceListRobustly():
    pageData = [
        # page, http code, json code, response page
        (-1, 200, CODE_ARG_INVALID['code'], 0),
        (0, 200, CODE_ARG_INVALID['code'], 0),
        (2**128, 200, CODE_ARG_INVALID['code'], 0),
        ('a', 200, CODE_ARG_TYPE_ERR['code'], 1),
        (100, 200, 0, 100)
    ]
    

    for page, httpCode, jsonCode, resPage in pageData:
        res = R.get(adviceUrl + f'?p={page}')
        assert res.status_code == httpCode
        if httpCode != 200: continue
        json = res.json()
        assert json['code'] == jsonCode, page
        if jsonCode != 0: continue
        assert json['page'] == resPage


@pytest.mark.robustTest
def testGetAdviceInfoRobustly():
    res = R.get(adviceUrl+'0/')
    assert res
    json = res.json()
    assert json['code'] == CODE_ADVICE_NOT_FOUND['code']


@pytest.mark.robustTest
def testResponseRobustly():
    res = R.post(adviceUrl + '0/', json={'response': ''})
    assert res
    json = res.json()
    assert json['code'] == CODE_ADVICE_NOT_FOUND['code']

    res = R.post(adviceUrl, json={'title': 'test res robustly', 'content': 'none'})
    assert res
    json = res.json()
    assert json['code'] == 0
    adviceId = json['advice-id']

    res = R.post(adviceUrl+f'{adviceId}/', json={})
    assert res
    json = res.json()
    assert json['code'] == CODE_ARG_MISSING['code']

    res = R.post(adviceUrl+f'{adviceId}/', json={'response': 54})
    assert res
    json = res.json()
    assert json['code'] == CODE_ARG_TYPE_ERR['code']