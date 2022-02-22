from config4test import R, UseAccount, baseUrl

def testDemo1():
    with UseAccount("normal_user"):          # 下面代码块中的所有请求都使用 normal_user 账号完成
        res = R.get(f"{baseUrl}profile/")    # 通过/profile/ 接口验证确实登陆了
        assert res
        assert res.json()["code"] == 0       # 正常返回，code 应该为 0
    
    res = R.get(f"{baseUrl}profile/")        # with 代码块之外，这个请求不使用任何账号
    assert res
    assert res.json()["code"] == 1           # 理应得到 code = 1，未登录

def testDemo2():
    # your test here ...
    pass

def someOtherFunc():
    pass