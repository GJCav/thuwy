# 鉴权后端设计文档

参考了OAuth Implicit Mode鉴权流程，有所删改，使用scope管理权限。



## 前端

> 详细API文档见后文。
>
> 使用Demo：/backend/test/thuwy-test/miniprogram/app.wxss (使用顾家铭的账号登录)

### 基本流程

1. 浏览器`POST /oauth/authorize/`，POST一个json到服务端，json参数如下：
   * scopes: list of required scope names
   
   * 例：
   
     ```json
     {
         "scopes": ["profile", "admin"]
     }
     ```
   
2. 服务端回传一个json，描述内容如下：
   * code: 错误码
   
   * scopes: `Scope`对象列表，用于描述申请权限的信息。例如：
   
     ```json
     {
         "scope": "profile",
        	"description": "基本用户信息"
     }
     ```
   
   * auth_code: 用于登陆的一串字符串
   
   * expire_at: 超时时间
   
3. 浏览器拿到上述信息，用二维码形式展示`auth_code`，要求用户使用小程序扫码登陆。
   同时，轮询`GET /oauth/authorize/<auth_code>/`，查询登录信息。
   
4. 用户使用小程序扫码，得到`auth_code`，`GET /oauth/authorize/<auth_code>/`得到授权信息，向用户展示授权信息，将用户确认授权或拒绝授权信息POST到后端，接口：`POST /oauth/authorize/<auth_code>/`。

5. 小程序授权(或拒绝)后，浏览器轮询将会得到一个json，其内容为：
   * access_token
   * expires_at
   
6. 之后需要鉴权的地方就在URL中带上一个参数`?access_token=<token>`即表示使用OAuth认证，否则使用session检查是否具有所需权限



### API列表

#### Scope对象

| 属性        | 类型 | 说明                       |
| ----------- | ---- | -------------------------- |
| scope       | str  | scope名，唯一标识权限/资源 |
| description | str  | 描述scope的附加信息        |





#### 申请OAuth

API：`POST /oauth/authroize/`

请求参数：JsonObject, 参数如下：

| 属性   | 类型      | 说明                |
| ------ | --------- | ------------------- |
| scopes | List[str] | 描述请求Scope的列表 |

例如：

```json
{"scopes": ["profile", "admin"]}
```

如果`scopes`列表中包含`*`，则会一次性获得授权用户的所有权限。
例如：

```json
{"scopes": ["*"]}
```

返回值：

| 属性      | 类型        | 说明                                 |
| --------- | ----------- | ------------------------------------ |
| code      | int         |                                      |
| errmsg    | str         |                                      |
| auth_code | str         | OAuth Code，用于后续授权流程         |
| scopes    | List[Scope] | Scope列表，Scope用于描述所需权限信息 |



#### 轮询授权情况

API: `GET /oauth/authorize/<auth_code>/`

请求参数：auth_code，即请求授权中返回的接口。

返回值：Json Object，其中`code`不同的值具有不同含义，

* `code=4` ，即CODE_ARG_MISSING

* `code=7`，即CODE_ARG_INVALID，表示后端找不到这个`auth_code`

* `code=401`，即CODE_OAUTH_REJECT，表示用户拒绝授权

* `code=402`，即CODE_OAUTH_HOLDON，表示用户还未授权，浏览器应继续轮询

* `code=0`，授权成功，返回其他属性如下：

  | 属性      | 类型             | 说明                           |
  | --------- | ---------------- | ------------------------------ |
  | token     | str              | Token                          |
  | expire_at | timestamp, int64 | token在expire_at之后失效       |
  | scopes    | List[Scope]      | Scope列表，描述得到授权的Scope |

注：这个接口小程序端也可使用



#### 小程序授权

> 这个接口要求请求Cookie中含有session id，详见*登录*部分API

API: `POST /oauth/authorize/<auth_code>/`

请求参数：

| 属性      | 类型 | 说明                   |
| --------- | ---- | ---------------------- |
| authorize | str  | 为`grant`表示允许授权  |
|           |      | 为`reject`表示拒绝授权 |

返回值：

| 属性      | 类型             | 说明                                   |
| --------- | ---------------- | -------------------------------------- |
| code      | int              |                                        |
| errmsg    | string           |                                        |
| token     | Token, str       | token字符串                            |
| expire_at | timestamp, int64 | 在此时间后，token失效，默认在7天后失效 |



#### Token使用

网页端示例代码：

```js
fetch("/some/api/xxxx/", {
    headers: {"Token": "<token string here>"}
}).then(res => {
    return res.json();
}).then(json => {
    console.log(json);
});
```

小程序端示例代码：

```json
wx.request({
    url: "/some/api/xxx/",
    header: {
        "Token": "<token string here>"
    },
    success(res){
        console.log(res.data);
    }
});
```



### 后端鉴权细节

现在同时使用`Session`、`Token`完成API权限管理，

* 若使用`Session`，需要在`Cookie`中附加Session信息
* 若使用`Token`，需要附加一个header，`Token: <token str>`

后端面对前端的一个请求，会优先使用`Session`进行鉴权，若请求中缺少`Session`，使用`Token`进行鉴权。

* 使用`Session`鉴权时，认为该请求拥有该用户所有`Scope`的访问权。
* 使用`Token`鉴权时，认为该请求只具有`OAuth`流程中声明的`Scope`的访问权。

如何选择鉴权方式？

* 对于小程序端，建议使用`Session`鉴权方式
* 对于网页端，因为`Cookie`有各种跨域文图，建议使用`Token`鉴权方式





## 后端

### 总览

#### ORM

相关数据库 & Model：`oauth_*`

| Model         | 表名            | 说明                     |
| ------------- | --------------- | ------------------------ |
| Scope         | oauth_scope     | 维护所有Scope信息        |
| Privilege     | oauth_privilege | 维护用户具有的Scope信息  |
| OAuthRequest  | oauth_req       | 维护OAuth请求            |
| OAuthReqScope | oauth_req_scope | 维护和OAuth中请求的Scope |
| OAuthToken    | oauth_token     | 维护所有Token            |



#### 后端如何加上鉴权？

**通过装饰器判断：**

示例代码：

```python
from app.auth import requireScope
from flask import g

@app.route("/some/api/xxxx/")
@requireScope(["profile admin", "operator"])
def someAPI():
    print(f'Client openid: {g.openid}')
    return {"data": "xxxx"}
```

上述代码表示`someAPI`需要满足下述条件*之一*：

* 同时具有`profile`、`admin`的Scope
* 具有`operator`的Scope

且可以使用`g.openid`获取用户的`openid`

> 过去代码中直接访问`session["openid"]`来获取OpenID，这只适用于Session鉴权的情况，现在请使用`g.openid`



**通过challengeScope判断**

```python
from app.auth import challengeScope
from flask import g

@app.route("/some/api/xxxx/")
def someAPI():
    if conditionA and challengeScope(["profile"]):
        ...
    elif condB and challengeScope(["admin", "teacher"]):
        ...
    else:
        return "权限不足"
```





### 数据库详情

#### 自定义类型

| 名称        | 类型        |
| ----------- | ----------- |
| OAUTH_CODE  | VARCHAR(24) |
| OAUTH_TOKEN | VARCHAR(24) |
| OAUTH_SCOPE | VARCHAR(64) |





#### 数据表

`OAuthRequest`

| field     | type             | description       |
| --------- | ---------------- | ----------------- |
| id        | int              | 自增ID            |
| code      | OAUTH_CODE       |                   |
| expire_at | timestamp, int64 |                   |
| reject    | int              | 0， default value |
|           |                  | 1，请求被用户拒绝 |



`OAuthReqScope`

| field    | type        | description                        |
| -------- | ----------- | ---------------------------------- |
| id       | int         | 自增ID                             |
| scope_id | int | 申请的scope的id               |
| req_id   | int         | 所属的`OAuthRequest` |
| token_id | int         | 初始为null，颁发token后关联到Token  |



`OAuthToken`

| field      | type     | description |
| ---------- | -------- | ----------- |
| id         | int      | 自增ID      |
| token      | TOKEN_STR |  |
| expired_at | INT64    |             |
| owner_id | OpenID, str | 授权用户的OpenID |
| req_id | int | 对应`OAuthRequest`的ID |



`Scope`

| field | type | description |
| ----- | ---- | ----------- |
| id | int | 自增ID |
| scope | SCOPE_STr, unique | Scope名 |
| description | VARCHAR(4096) | 附加描述信息 |

特殊`Scope`：

* profile：表示已经登录，所有用户默认具有这个权限。但`Privilege`表中没有这一行，`profile`是程序运行时自动添加的。
* `*`：在授权时被替换为一个用户所具有的所有`Privilege`


`Privilege`

| field | type | description |
| ----- | ---- | ----------- |
| id | int | 自增ID |
| openid | OpenID |表明OpenID对应用户具有该Scope的权限|
| scope_id | int |对应Scope的ID|




#### 添加一个新Scope并授权特定用户

1. 打开`/backend/app/auth/__init__.py::init_sys_account()`
   在下述内容添加一行

   ```python
   scopes = [
       {"scope": "scope name", "des": "description here"},
       ...
   ]
   ```

2. 用`mysql`终端中给`oauth_privilege`表插入一行

   ```mysql
   INSERT INTO oauth_privilege VALUES (null, "openid here", <scope id here>);
   ```



## 现有Scope/Privilege

* `profile`, 只要登录，都具有此权限。
* `*`：一个新号，如果OAuth请求中包含这个scope，最后用户授权时将一次性授予该用于拥有的所有privilege，主要是为了方便网页端开发，这样就只用登陆&授权一次。 
* `admin`：表示管理员权限，一些老旧API大量使用这个scope。
* `congyou`：从游坊管理权限，包括从游坊的发布、修改等。
* `dayi`：答疑坊管理权限，包括提问的回答、审核、公开等。