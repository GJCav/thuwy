
from config4test import R, baseUrl
import pytest

adviceUrl = baseUrl + 'advice/'

adviceIds = []

def testAddAdvice():
    adviceCount = 10
    for i in range(adviceCount):
        reqJson = {
            'title': f'add advice {i}',
            'content': f'tead add advice'
        }
        res = R.post(adviceUrl, json=reqJson)
        assert res
        json = res.json()
        assert json['code'] == 0, json

        adviceIds.append(json['advice-id'])

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
            assert advice.keys() == {'id', 'proponent', 'title', 'state', 'response'}
            curIdSet.add(advice['id'])

        idSet -= curIdSet

    assert len(idSet) == 0, f'建议列表没有完整显示添加的advice，未找到：{idSet}'

def testGetAdviceInfo():
    for id in adviceIds:
        res = R.get(adviceUrl + f'{id}')
        assert res
        json = res.json()
        assert json['code'] == 0, json
        
