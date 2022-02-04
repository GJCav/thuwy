import requests as R
from pprint import pprint

def testReqOAuth():
    res = R.post('http://127.0.0.1:5000/oauth/authorize/', json={
        'scopes': ['profile', 'admin']
    })
    assert res
    json = res.json()
    pprint(json)
    assert json
    assert json['code'] == 0
    assert json['scopes']
    assert json['auth_code']
    assert json['expire_at']

    for e in json['scopes']:
        assert isinstance(e, dict)
        assert 'scope' in e
        assert 'description' in e


testReqOAuth()