## 鉴权

### 登陆

**Des:** 第一次登陆

**API:** `POST /login/`

**请求参数：** Json Object

| 属性 | 类型   | 必填 | 说明                                                         |
| ---- | ------ | ---- | ------------------------------------------------------------ |
| code | string | 是   | 小程序调用 wx.login 获取的code，见[微信文档](https://developers.weixin.qq.com/miniprogram/dev/api/open-api/login/wx.login.html#%E5%8F%82%E6%95%B0) |

 **返回值：** Json Object，其中包含：

| 属性      | 类型   | 可否省略 | 说明                                                         |
| --------- | ------ | -------- | ------------------------------------------------------------ |
| code      | int    | 否       | 错误码                                                       |
| errmsg    | string | 否       | 错误信息                                                     |
| wx-code   | int    | 是       | 微信接口返回的错误码，见[微信文档中errcode部分](https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/login/auth.code2Session.html) |
| wx-errmsg | string | 是       | 微信接口返回的错误信息，同上                                 |
| bound     | bool   | 否       | 用户是否已经绑定学号、姓名                                   |

**错误码说明** ：

| code    | errmsg                            | 说明                                               |
| ------- | --------------------------------- | -------------------------------------------------- |
| ~~101~~ | ~~code missing~~                  | ~~未将wx.login()获得的code上传到服务器或格式错误~~ |
|         |                                   | 已废弃，见 code = 4 的说明                         |
| 102     | 请求微信超时                      | 服务器调用微信API超时                              |
| 103     | 链接微信失败                      | 服务器网络异常                                     |
| 201     | 请求微信失败                      | 微信返回了非200的响应                              |
| 202     | 微信返回信息不完整                | 微信返回的数据不全                                 |
| 203     | 微信拒绝了服务器                  | 微信拒绝了服务器，此时有wx-\*属性                  |
| 200     | 未知错误，丢人gjm没有考虑这个情况 | 服务器出现未知的异常                               |

**Set-Cookie？：** True

该接口会设置形如`session=xxxxx`的Cookie作为登陆信息，下文调用要求`Login?:True`的接口时，需要把这个Cookie传回给后端。

> 这个cookie包含了flask加密的openid和微信返回的session_key



**实例代码：**

登陆：

```js
function onLogin() {
  wx.login({ // 调用微信的登陆API
    timeout: 5000,
    success(res) {
      if (res.code) {
        wx.request({
          url: 'http://127.0.0.1:5000/login/', // 这里填服务器地址或测试测试
          timeout: 3000,
          data: { code: res.code }, // 把微信返回的code传给服务器
          method: 'POST',
          success(o) {
            //console.log(o);
            //本地储存后端传回的第一个cookie，对应session信息，便于后续使用
            wx.setStorageSync('cookie', o.cookies[0]);
          },
          fail() {
            console.log('fail to com backend')
          }
        })
      } else {
        console.log('fails');
      }
    }
  })
};
```

之后要求登陆的地方只要这么做：

```js
wx.request({
  url: 'http://127.0.0.1:5000/bind/', // API 地址
  method: 'POST',
  header: {
    'content-type': 'application/json; charset=utf-8',
    'cookie': wx.getStorageSync('cookie') // 这里取出储存的登陆信息，传给服务器
  }
  //...其他代码
});
```



一次登陆后过多久需要重新登陆还在纠结(ー`´ー)，先不管吧。



### 绑定

**Des:**  设置用户的学号、姓名、班级

**API:** `POST /bind/`

**要求：** 先完成登录步骤，带上`Session`信息

**请求参数:** Json Object

| 属性  | 类型   | 必填 | 说明 |
| ----- | ------ | ---- | ---- |
| id    | string | 是   | 学号 |
| name  | string | 是   | 姓名 |
| clazz | string | 是   | 班级 |

**注：** 绑定时服务器会根据已有的数据库核验上述三个属性是否相互匹配，匹配才予以通过。



**返回值:** Json Object，其中包含属性：

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |

**错误码说明：**

| code | errmsg       | 说明                                 |
| ---- | ------------ | ------------------------------------ |
| 101  | 请勿重复绑定 | 用户已经绑定过信息了                 |
| 102  | 信息已被绑定 | 欲绑定的学号、姓名、班级已经被绑定了 |
| 103  | 绑定信息错误 | 学号、姓名、班级不匹配或有错误       |

### UserProfile 对象

用户档案对象，包含属性如下：

| 属性      | 类型   | 说明         |
| --------- | ------ | ------------ |
| name      | string | 姓名         |
| clazz     | string | 班级         |
| school-id | string | 学号         |
| admin     | bool   | 是否为管理员 |
| openid    | string | 用户的openid |



### 获取本人档案

**API**: `GET /profile/`

**Des：** 获取当前用户信息

**Scope: ** profile

**请求参数：** 无

**返回值：** 附加错误信息的`UserProfile`对象。



### 获取他人档案

**API**: `GET /profile/<open-id>/`

**Des：** 获取其他用户信息

**Scope:** ["profile admin"]

**请求参数：** open-id，目标用户的openid

**返回值：** Json Object，同`GET /profile/`



### 成为管理员

**Des:** 申请当前用户成为管理员

**API:** `POST /admin/request/`

**Scope:** profile

**请求参数：** 无

**返回值：** Json Object，属性如下：

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |
| id     | int    | 申请id   |

申请后，该请求会加入等待审核清单，等待其他管理员通过后该用户成为管理员。



### 管理员请求列表

**API:** `GET /admin/request/`

**Scope:** ["profile admin"]

**请求参数:** 无

**返回值：** Json Object，属性如下：

| 属性   | 类型       | 说明             |
| ------ | ---------- | ---------------- |
| code   | int        | 错误码           |
| errmsg | string     | 错误信息         |
| list   | json array | 包含AdminReq对象 |

AdminReq属性：

* id, 请求id
* requestor，申请者的profile
* approver, 审核者，可能为空
* reason, 审核批语，可能为空

**返回值：** Json Object，属性如下：

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |





### 审核管理员

**Des:** 决定某用户是否通过管理员审核。

**API:** `POST /admin/request/<requst-id>/` 

**Scope:** ["profile admin"]

**请求参数:** Json Object，

| 属性   | 类型   |                              |
| ------ | ------ | ---------------------------- |
| pass   | int    | 是否通过，1 为通过，0 为拒绝 |
| reason | string | 理由                         |

**返回值：** Json Object，属性如下：

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |



### 获取管理员列表

**API：** `GET /admin/`

**Scope:** ["profile"]

**返回值：**

| 属性     | 类型       | 说明           |
| -------- | ---------- | -------------- |
| code     | int        | 错误码         |
| errmsg   | string     | 错误信息       |
| profiles | Json Array | 用户档案列表。 |



### 删除管理员

**API:** `DELETE /admin/<open-id>/`

**Scope:** ["profile admin"]

**请求参数：** open-id，要删除的管理员id

**返回值：** Json Object，属性如下：

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |





### 获取用户列表

**API：** `GET /user/?clazz=<class>&p=<page>`

**Scope:** ["profile admin"]

**Args：** 

| 属性  | 类型   | 说明                     |
| ----- | ------ | ------------------------ |
| clazz | string | 根据班级筛选，默认不筛选 |
| p     | int    | 页数，默认为1            |

返回用户数可能非常多，进行分页，每页最多30个用户。

**返回值：**

| 属性     | 类型       | 说明                                      |
| -------- | ---------- | ----------------------------------------- |
| code     | int        | 错误码                                    |
| errmsg   | string     | 错误信息                                  |
| profiles | Json Array | 用户档案列表，包含多个`UserProfile`对象。 |



### 解绑用户

**API：** `delete /user/<openid>/`

**Des：** 删除该用户的绑定关系。

**Scope:** ["profile admin"]

**Args：** 

| 属性   | 类型   | 说明         |
| ------ | ------ | ------------ |
| openid | string | 用户的OpenID |

**返回值：**

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |

**错误码：**

| code | errmsg     |
| ---- | ---------- |
| 301  | 用户不存在 |
