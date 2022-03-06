# 测试脚本编写教程

## 基本框架

我们这个可以说是半自动化测试，基本思路就是python模拟前端发送一系列的请求给后端，检验后端的返回结果，从而测试后端。

HTTP框架`requests`，测试框架`pytest`。



## 快速开始

### 配置服务器URL

打开`config4test.py`，进行一些基本配置，该文件前几行如下：

```python
localTest = "http://127.0.0.1:8989/"
remoteTest = "https://dev-api.thuwy.top/"
baseUrl = remoteTest
```

* localTest: 本地测试URL，这里主要是改一下端口，IP基本都是`127.0.0.1`
* remoteTest: 远程测试URL，本地测试完成之后需要进行远程测试，需要填写测试服务器地址
* baseUrl: 提供给测试脚本使用的URL

注意：所有的URL结尾统一加上`/`；测试服务器是`https`，本地服务器是`http`。



### 查看实例代码

打开`guide.py`，文件内容如下：

```python
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
```

第一行依次导入了：

* R，是经过一些修改后的`requests`库，以支持后续的`UseAccount`功能。
* `UseAccount`，用于快速切换到测试账号的一个类，使用方法见代码。
* `baseUrl`，服务器地址。



### 执行测试

在`pytest`框架下，测试脚本不能直接通过`python`指令运行，而是使用`pytest`指令运行。对于上述测试脚本，可以这么运行：

```bask
cd backend/test
pytest guide.py
```

不出意外的话可以看到如下输出：

```
================================= test session starts ==================================
platform linux -- Python 3.8.10, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
rootdir: /home/jcav/thuwy/backend/test, configfile: pytest.ini
collected 2 items                                                                      

guide.py::testDemo1 PASSED                                                       [ 50%]
guide.py::testDemo2 PASSED                                                       [100%]

================================== 2 passed in 0.29s ==================================
```

绿色的PASSED表示测试通过，红色的FAILED表示有错误等等，大家都看得懂英文，这里就不多说了。



上述指令解释如下：

```bask
pytest guide.py
```

表示执行`guide.py`单个测试脚本，且文件中每个以`test`开头的函数都会作为单独的case被执行，`someOtherFunc`被忽略。



如果使用下述指令：

```bask
pytest .
```

表示执行当前文件下所有名称形如`testXXXX.py`的测试脚本，如果脚本文件名称不以`test`开头，不会被执行。



如果只要执行单个文件中的单个函数，可以这么做：

```bask
pytest guide.py::testDemo1
```



## Reference

上面的只是一个Quick Start，更多信息可以参考官方文档：

* [Requests](https://docs.python-requests.org/en/latest/)
* [pytest](https://docs.pytest.org/en/7.0.x/)



