# 鉴权

> Author: JCav
>
> LastUpdate: 20220719



## 基本用户信息

### 登陆

**Des:** 第一次登陆

**API:** `POST /login/`

**请求参数：** Json **Object**

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

用户档案对象，包含属性如下：****

| 属性           | 类型        | 说明                             |
| -------------- | ----------- | -------------------------------- |
| name           | string      | 姓名                             |
| clazz          | string      | 班级                             |
| school-id      | string      | 学号                             |
| admin          | bool        | 是否为管理员                     |
| openid         | string      | 用户的openid                     |
| privilege_info | json object | 用户的权限信息（包含组权限信息） |



### 获取本人档案

**API**: `GET /profile/`

**Des：** 获取当前用户信息

**Scope: ** `User`

**请求参数：** 无

**返回值：** `UserProfile`对象



## 用户管理

### 用户基本信息管理

#### 获取他人档案

**API**: `GET /profile/<open-id>/`

**Des：** 获取其他用户信息

**Scope:** `["UserAdmin"]`

**请求参数：** open-id，目标用户的openid

**返回值：** Json Object，同`GET /profile/`



#### 获取用户列表

**API：** `GET /user/?clazz=<class>&p=<page>`

**Scope:** `UserAdmin`

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



#### 解绑用户

**API：** `delete /user/<openid>/`

**Des：** 删除该用户的绑定关系。

**Scope:** `UserAdmin`

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



### 用户权限(Scope)管理

#### 列出用户权限

**API：** `GET /user/<openid>/scope/`

**Scope:** `ScopeAdmin`

**返回值：** Json Object，有`scopes`属性，类型为`List[PrivilegeInfo]`，表示用户的所有权限；同时附加错误信息。

其中，`PrivilegeInfo` 格式为：
```json
{
  "expire_at": 0, // 权限超时时间，0 表示长期有效
  "scope": {
      "create_time": 1660661029423,
      "description": "Basic user permission",
      "name": "User"
  }
}
```

**错误码：**

| code | errmsg     |
| ---- | ---------- |
| 301  | 用户不存在 |



#### 添加用户权限

**API：** `POST /user/<openid>/scope/`

**Scope:** `ScopeAdmin`

**POST Payload：** Json Object, 包含`scope`字段，属性为`str`，表示要添加的`Scope`名称。

**返回值：** Json Object，包含`scopes`字段，属性为`List[str]`，表示修改后用户具有的所有权限。

**错误码：**

| code | errmsg               |
| ---- | -------------------- |
| 301  | 用户不存在           |
| 421  | 用户已经具有这个权限 |
| 411  | 不存在这个Scope      |



#### 撤销用户权限

**API：** `DELETE /user/<openid>/scope/<scope>/`

**Scope:** `ScopeAdmin`

**返回值：** Json Object，包含`scopes`字段。

**错误码：**

| code | errmsg             |
| ---- | ------------------ |
| 301  | 用户不存在         |
| 422  | 用户不具备指定权限 |



## 组权限管理

该小节API除非特殊说明，权限统一要求`ScopeAdmin`

### 组管理

**新建组**： `POST /auth/group/`

**删除组**： `DELETE /auth/group/<group_name>/`

**组列表**：`GET /auth/group/?regex=<re_expr>`

**组信息**：`GET /auth/group/<group_name>/`



#### 新建组

API：`POST /auth/group/`

Post Payload: Json  Object

| name      | type            | description |
| --------- | --------------- | ----------- |
| name      | string          | 组名        |
| expire_at | timestamp, 可选 | 超时时间    |

返回错误码：

| code | msg          | description |
| ---- | ------------ | ----------- |
| 401  | 已存在同名组 |             |



#### 删除组

API： `DELETE /auth/group/<group_name>/`

错误码：

| code | msg          | description |
| ---- | ------------ | ----------- |
| 402  | 找不到这个组 |             |



#### 组列表

API：`GET /auth/group/?regex=<re_expr>`

Param: 

* re_expr，正则表达式，注意url encode
* p，分页，默认为 1

Response Body: 形如：

```json
{
    "code": 0,
    "errmsg": "成功",
    "groups": [
        {
            "expire_at": 0,
            "id": 3,
            "name": "group_1",
            "type": "Group"
        },
        ...
    ]
}
```



#### 组信息

API：`GET /auth/group/<group_name>/`

```json
{
    "code": 0,
    "errmsg": "成功", 
    "expire_at": 0, // 超时时间
    "id": 3,
    "members": [ // 成员信息
        {
            "clazz": "未央-测试01",
            "email": null,
            "name": "normal_user",
            "openid": "normal_user",
            "school-id": "2020018888"
        },
        ...
    ],
    "name": "group_1", // 组名
    "privileges": [ // 组权限信息
        {
            "expire_at": 0,
            "scope": {
                "create_time": 1660661029423,
                "description": "Basic user permission",
                "name": "User"
            }
        },
        //...
    ],
    "type": "Group"
}
```







### 组权限管理

**列举权限**： 通过组信息API获取

**添加权限**： `POST /auth/group/<group_name>/scope/`

**删除权限**： `DELETE /auth/group/<group_name>/scope/<scope_name>/`



#### 添加权限

API：`POST /auth/group/<group_name>/scope/`

POST Payload：

| name      | type                    | description |
| --------- | ----------------------- | ----------- |
| scope     | string                  | scope 名    |
| expire_at | timestamp, 可选，默认 0 | 超时时间    |



#### 删除权限

API:  `DELETE /auth/group/<group_name>/scope/<scope_name>/`





### 组员管理

**列举组员**： 通过组信息API获取

**添加组员**： `POST /auth/group/<group_name>/member/`

**删除组员**： `DELETE /auth/group/<group_name>/member/<openid>/`



#### 添加组员

API:  `POST /auth/group/<group_name>/member/`

POST payload:

| name      | type            | description  |
| --------- | --------------- | ------------ |
| openid    | string          | 用户的openid |
| expire_at | timestamp, 可选 | 超时时间     |



## 域管理

### 列出所有域

API：`GET /auth/scope/?regex=<re_expr>`
