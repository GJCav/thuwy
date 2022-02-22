from config4test import R, UseAccount, baseUrl

def testDemo():
    with UseAccount("normal_user"):
        res = R.get(f"{baseUrl}profile/")
        assert res
        assert res.json()["code"] == 0
    
    res = R.get(f"{baseUrl}profile/")
    assert res
    assert res.json()["code"] == 1
