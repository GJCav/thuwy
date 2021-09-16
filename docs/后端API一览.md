# API 约定

* [API 约定](#api-约定)
  * [鉴权](#鉴权)
    * [登陆](#登陆)
    * [绑定](#绑定)
    * [获取本人档案](#获取本人档案)
    * [获取他人档案](#获取他人档案)
    * [成为管理员](#成为管理员)
    * [管理员请求列表](#管理员请求列表)
    * [审核管理员](#审核管理员)
    * [删除管理员](#删除管理员)
    * [使用测试账号登录](#使用测试账号登录)
  * [物品管理](#物品管理)
    * [Item对象](#item对象)
    * [物品列表](#物品列表)
    * [物品详细信息](#物品详细信息)
    * [添加物品](#添加物品)
    * [修改物品](#修改物品)
    * [删除物品](#删除物品)
    * [查询物品预约信息](#查询物品预约信息)
  * [预约](#预约)
    * [Rsv对象](#rsv对象)
    * [RsvMethod对象](#rsvmethod对象)
      * [对象说明](#对象说明)
      * [对应的interval格式](#对应的interval格式)
    * [RsvId 对象](#rsvid-对象)
    * [RsvState 对象](#rsvstate-对象)
    * [提交预约](#提交预约)
    * [查询我的预约](#查询我的预约)
    * [预约详细信息](#预约详细信息)
    * [取消预约](#取消预约)
    * [管理员查看预约](#管理员查看预约)
    * [管理员更改预约状态](#管理员更改预约状态)
  * [建议](#建议)
    * [Advice 对象](#advice-对象)
    * [错误码说明](#错误码说明)
    * [管理员获取建议列表](#管理员获取建议列表)
    * [用户提交建议](#用户提交建议)
    * [用户获取建议列表](#用户获取建议列表)
    * [获取建议详细信息](#获取建议详细信息)
    * [回复建议](#回复建议)
  * [Carousel](#carousel)
    * [Carousel 对象](#carousel-对象)
    * [获取Carousel列表](#获取carousel列表)
    * [添加Carousel](#添加carousel)
    * [修改Carousel](#修改carousel)
    * [查看Carousel详细信息](#查看carousel详细信息)
    * [查看历史Carousel](#查看历史carousel)
  * [错误码](#错误码)

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

**Login?:** True

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

### UserProfile 对象

用户档案对象，包含属性如下：

| 属性      | 类型   | 说明         |
| --------- | ------ | ------------ |
| name      | string | 姓名         |
| clazz     | string | 班级         |
| school-id | string | 学号         |
| admin     | bool   | 是否为管理员 |



### 获取本人档案

**API**: `GET /profile/`

**Des：** 获取当前用户信息

**Login:** True

**请求参数：** 无

**返回值：** 附加错误信息的`UserProfile`对象。



### 获取他人档案

**API**: `GET /profile/<open-id>/`

**Des：** 获取其他用户信息

**Login:** True, 有管理员权限

**请求参数：** open-id，目标用户的openid

**返回值：** Json Object，同`GET /profile/`



### 成为管理员

**Des:** 申请当前用户成为管理员

**API:** `POST /admin/request/`

**Login:** True，且需要绑定

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

**Login:?** True, 有管理员权限

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

**Login?:** True, 需要绑定，需要为管理员

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

**Login：** True，且绑定，且登录。

**返回值：**

| 属性     | 类型       | 说明           |
| -------- | ---------- | -------------- |
| code     | int        | 错误码         |
| errmsg   | string     | 错误信息       |
| profiles | Json Array | 用户档案列表。 |



### 删除管理员

**API:** `DELETE /admin/<open-id>/`

**Login:** 登陆绑定，且有管理员权限

**请求参数：** open-id，要删除的管理员id

**返回值：** Json Object，属性如下：

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |



### 使用测试账号登录

**API：** `GET /test/login/?mode=[user|admin]`

**Des：**

当后端的配置为`TestConfig`时这个接口存在，使用这个接口可以创建一个和微信openid无关的测试账号。这些用于测试的账号将会在产品正式上线前删除。

**Args:** mode，为user或其他值时创建拥有用户权限的账号，为admin时创建管理员账号。

**Set-Cookie?** True

**返回值：**

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |



### 获取用户列表

**API：** `GET /user/?clazz=<class>&p=<page>`

**Login:** True，且绑定，且为管理员

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

**Login:** True，且绑定，且为管理员

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





## 物品管理

### Item对象

Item对象是一个Json Object对象，包含如下属性：

| 属性        | 类型        | 说明                                               |
| ----------- | ----------- | -------------------------------------------------- |
| name        | string      | 名字                                               |
| id          | ItemId      | 设备id                                             |
| available   | bool        | 设备是否可用，如果设备被下架，为0                  |
| delete      | bool        | 是否删除设备，只在`POST /item/`且是删除操作时存在  |
| brief-intro | string      | 简要介绍，小于50字符                               |
| md-intro    | string      | 详细介绍，只在`/item/mdintro`返回                  |
| thumbnail   | url, string | 缩略图的url                                        |
| rsv-method  | RsvMethod   | 支持的预约方式                                     |
| attr        | int         | 特殊属性                                           |
| group       | string      | 所在组名称，若无组，为null或没有内容的字符串，即“” |



### 物品列表

> 我们把所有能被预约的东西都称之为 `item` ，包括摄像机、29号楼房间等。

**Des:** 获取物品列表

**API**： `GET /item/?p=<page>&group=<group>`

**Login?:**  False

**请求参数**：

| 属性  | 类型   | 必填              | 说明                                       |
| ----- | ------ | ----------------- | ------------------------------------------ |
| p     | int    | 否，不填写默认为1 | 分页获取，避免一次性数据过多，每页20条数据 |
| group | string | 否                | 限定范围为指定分组                         |

**返回值:** Json Object，其中包含：

| 属性       | 类型       | 说明           |
| ---------- | ---------- | -------------- |
| code       | int        | 错误码         |
| errmsg     | string     | 错误信息       |
| item-count | int        | item的总个数   |
| page       | int        | 返回的是第几页 |
| items      | Json Array | 包含`Item`对象 |



### 物品详细信息

**API:** `GET /item/<item-id>/`

**Des：** 获取物品详细信息，包括`md-intro`、`delete`、`attr`属性

**Login?：** False

**请求参数：** 无

* `item-id`：要查询的物品id

**返回值：** Json Object，包含属性如下

| 属性   | 类型         | 说明     |
| ------ | ------------ | -------- |
| code   | int          | 错误码   |
| errmsg | string       | 错误信息 |
| item   | Item, Object | Item对象 |

**错误码说明：**

| code | errmsg     | 说明                |
| ---- | ---------- | ------------------- |
| 101  | 未找到物品 | 指定的item-id不存在 |



### 添加物品

**Des：** 添加物品

**API：** `POST /item/`

**Login?:** True，且绑定，且是管理员

**请求参数：** Item，包含且只包含如下属性：

* name
* brief-intro
* md-intro
* thumbnail
* rsv-method
* attr，可选参数，默认为 0
* group，可选参数，默认为null

**返回参数：**

| 属性    | 类型          | 说明         |
| ------- | ------------- | ------------ |
| code    | int           | 错误码       |
| errmsg  | string        | 错误信息     |
| item-id | ItemID, int64 | 添加的物品ID |

**错误码说明**

| code | errmsg         | 说明                |
| ---- | -------------- | ------------------- |
| 101  | item not found | 指定的item-id不存在 |



### 修改物品

**API:** `POST /item/<item-id>/`

**Des：** 修改物品信息

**Login?：** True，要求绑定、登陆

**请求参数：** 

* **ARG：** item-id，物品id

* **Body：** Rsv，只能包含下表属性，不需要修改的属性可以省略
  * name
  * available
  * brief-intro
  * md-intro
  * thumbnail
  * rsv-method
  * attr
  * group，设为null或空字符串表示取消分组

**返回值：** Json Object，包含属性如下

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |

**错误码说明：**

| code | errmsg     | 说明                |
| ---- | ---------- | ------------------- |
| 101  | 未找到物品 | 指定的item-id不存在 |



### 删除物品

**API:**  `DELETE /item/<item-id>/`

**Des：** 删除物品

**请求参数：** item-id，物品id

**返回值：** Json Object，包含属性如下

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |

**错误码说明：**

| code | errmsg     | 说明                |
| ---- | ---------- | ------------------- |
| 101  | 未找到物品 | 指定的item-id不存在 |



### 查询物品预约信息

**API:**  `GET /item/<item-id>/reservation/`

**Des：** 查询某个物品未来7天的预约信息

**Des:** 查询某个物品未来一周的预约信息。

**Login?:** False

**请求参数：** Json Object，属性如下：

| 属性    | 类型  | 必填 | 说明           |
| ------- | ----- | ---- | -------------- |
| item-id | int64 | 是   | 要查询的物品id |

**返回值：** Json Object，属性如下：

| 属性   | 类型       | 说明                                |
| ------ | ---------- | ----------------------------------- |
| code   | int        | 错误码                              |
| errmsg | string     | 错误信息                            |
| rsvs   | Json Array | 包含Rsv对象，返回未来一周的预约信息 |

此时Rsv对象只包含如下属性：

* id
* method
* state
* interval



## 预约

### Rsv对象

Rsv对象是一个Json Object，包含如下属性：

| 属性     | 类型      | 说明                             |
| -------- | --------- | -------------------------------- |
| id       | RsvId     | 这个预约的编号                   |
| item     | string    | 预约物品的名字                   |
| item-id  | int64     | 物品ID                           |
| guest    | string    | 预约人的名字                     |
| reason   | string    | 预约理由                         |
| method   | RsvMethod | 使用的预约方法，保证只有一位为 1 |
| state    | RsvState  | 预约状态                         |
| interval | Any       | 具体类型、含义根据RsvMethod确定  |
| approver | string    | 审核员姓名                       |
| exam-rst | string    | 审核批语                         |



### RsvMethod对象

#### 对象说明

RsvMethod是一个32位的无符号整数（可以更长，但我觉得没必要），每一位是否为 1 代表是否支持对应的预约方法。现在存在的几种预约方法：

| 占用数据位 | 说明                                                         |
| ---------- | ------------------------------------------------------------ |
| 0          | 时间段预约，一次可预约多个时间段。                           |
|            | 周一到周周五分为：早上(8-12)，中午(13-17)、晚上(17-23)       |
|            | 周末两天作为整体预约。                                       |
| 1          | 灵活预约：预约某一天内某一个时间段，预约精确到分钟。         |
|            | 例如：`2021-7-18 8:30-22:35`含义为预约18号早上8点半到晚10：35。 |

如果一个RsvMethod值为 3，则意味着这个Item即可以按照时间段预约、又可以灵活预约，因为 `3 = 0b11`。如果为 2 ，则意味着只支持灵活预约。

#### 对应的interval格式

**1. 时间段预约：**

RsvMethod = 1

interval 是一个Json Array，其中每一个元素的格式：`yyyy-mm-dd c`

 - yyyy：年份

 - MM：月份，从 1 开始编号

 - dd：日期，从 1 开始编号

 - c：时间段编号，值为：

   - 1：上午
   - 2：下午
   - 3：晚上
   - 4：周末整体

   且 c = 4 时，yyyy-mm-dd 日期对应周末两天中的周六日期。

例：`2021-8-12 2`表示预约21年8月下午时间段。



**2. 灵活预约**

RsvMethod = 2

interval 格式：`yyyy-mm-dd HH:MM-HH:MM`

	* yyyy-mm-dd：年月日，月份和日期从 1 开始编号

 * HH:MM-HH:MM：预约的开始、结束时间
   * HH：小时，24小时制，范围 \[0, 23]
     	* MM：分钟，范围 \[0, 59]
     	* 要求开始时间早于结束时间





### RsvId 对象

RsvId是一个int64，每一位有不同的含义，具体会仿照snowflake算法设计。

基本上是`时间戳+机器码+自增编号`的设计，但机器码会被砍的很严重，反正我们就一个服务器¯\\_(ツ)_/¯。

具体每一个数据位含义如下：

```
0000 0000 0000 0000
  60        52
0000 0000 0000 0000 
  44        36
0000 0000 0000 0000
  28        20
0000 0000 0000 0000
  12         4

52-13: 40 位时间戳，毫秒，从2020.1.1 00:00:000 开始计时
12- 8: 5  位机器码，0-63，但我们只有一台机器，所以都是0
7 - 0: 8  位流水号，0-255，自动递增，递增慢时会阻塞线程
```



### RsvState 对象

**已经更新到新版本，详见`docs/订单状态.*`**



### 提交预约

**API:**  `POST /reservation/`

**Des:** 提交一个预约

**Login?:** True，且需要事先绑定姓名学号。

**请求参数** ：Rsv对象，只需包含如下属性，其余省略：

| 属性     | 类型           | 说明                                  |
| -------- | -------------- | ------------------------------------- |
| item-id  | int64          | 要预约物品的id                        |
| reason   | string         | 预约理由                              |
| method   | RsvMethod, int | 使用的预约方法，二进制下只能有一位为1 |
| interval | any            | 描述预约时间段，格式由method决定      |

**返回值** ：Json Object，属性如下：

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |
| rsv-id | RsvId  | 预约ID   |

**错误码说明：** 

| code | errmsg         | 说明                                        |
| ---- | -------------- | ------------------------------------------- |
| 101  | 时间冲突       | 预约时间冲突                                |
| 102  | 超出预约时限   | 不允许预约过去的时间且不允许预约7天后的时间 |
| 103  | 预约方法重复   | method包含多个预约方法                      |
| 201  | 预约方法不支持 | 想要预约的物品不存在                        |





### 查询我的预约

**Des:** 查询“我的”所有预约

**API:** `GET /reservation/me/?st=<start-time>&ed=<end-time>&state=<state>/`

**Login?**: True

**请求参数**:

| 属性  | 类型          | 必填 | 说明                                   |
| ----- | ------------- | ---- | -------------------------------------- |
| st    | 时间戳, int64 | 否   | 查询st之后提交的预约，不填则不设上限   |
| ed    | 时间戳, int64 | 否   | 查询截止ed前提交的预约，不填则不设下限 |
|       |               |      | st、ed格式：yyyy-mm-dd                 |
|       |               |      | 注：上面筛选的是**提交预约的时间**。   |
| state | RsvState      | 否   | 查询状态为state的预约                  |

**返回值：** Json Object，包含属性如下：

| 属性   | 类型       | 说明                                  |
| ------ | ---------- | ------------------------------------- |
| code   | int        | 错误码                                |
| errmsg | string     | 错误信息                              |
| my-rsv | Json Array | 包含`Rsv`对象，为需要查询的预约信息。 |

注：此时`Rsv`对象不包含`guest`属性



### 预约详细信息

**API**: `GET /reservation/<rsv-id>/`

**Des：** 获取某个预约的详细信息

**Login?：** False

**请求参数：** `rsv-id`

**返回值：** Json Object，属性如下：

| 属性   | 类型   | 说明       |
| ------ | ------ | ---------- |
| code   | int    | 错误码     |
| errmsg | string | 错误信息   |
| rsv    | Rsv    | 查询的预约 |

**错误信息说明：** 

| code | errmsg       | 说明               |
| ---- | ------------ | ------------------ |
| 201  | 未找到该预约 | 没有找到对应的预约 |





### 取消预约

**Des:** 取消一个预约

**API:** `DELETE /reservation/<rsv-id>/`

**Login?:** True，且要求绑定

**请求参数：** Json Object，包含如下属性：

| 属性   | 类型  | 必填 | 说明             |
| ------ | ----- | ---- | ---------------- |
| rsv-id | RsvId | 是   | 要取消的预约编号 |

**返回值：** Json Object，包含属性如下：

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |

**错误码说明：**

| code | errcode      | 说明           |
| ---- | ------------ | -------------- |
| 201  | 未找到该预约 | 不存在这个预约 |
| 202  | 预约已开始   | 预约已经开始   |
| 203  | 预约已结束   | 预约已经完成   |
| 204  | 预约被拒绝   | 预约被审核拒绝 |





### 管理员查看预约

**API:** `GET /reservation/?st=<start-time>&<ed-time>&state=<state>&method=<method>&p=<page>/`

**Des：** 查询预约时间介于`st`和`ed`间的预约

> 注意：不是 提交预约 的时间，这个和`GET /reservation/me`的有所不同，之后可能会修改`GET /reservation/me`的约定。

**Login?:** True，绑定、且为管理员

**请求参数：** 一下参数都是可选的。

* st：限定在该时间之后开始的预约

* ed：限定在该时间之前结束的预约

  以上两个时间格式均满足yyyy-mm-dd，表示的时间都为该日期的 00:00 时刻

* state：筛选状态，状态码见RsvState；匹配规则为 `Rsv.state & state > 0` 则入选

* method: 筛选预约使用的方法

* p：返回的结果可能会很多，对结果分页，每页20条记录左右，该参数用于指定第几页



**返回值：** Json Object, 

| 属性   | 类型       | 说明           |
| ------ | ---------- | -------------- |
| code   | int        | 错误码         |
| errmsg | string     | 错误信息       |
| page   | int        | 返回的是第几页 |
| rsvs   | Json Array | 包含`Rsv`对象  |

> 为啥每页的记录数不确定？为什么不返回一个rsv-count指明查询到的订单总数？
>
> 因为一个LongTimeRsv会被拆分，在查询时经过合并和补足（比如一个LongTimeRsv只有一部分在查询时间内），记录条数就不好说了，但可以明确的是恰当选取p的值，rsvs返回一个空列表时，表示已经查询到所有结果了。
>
> 注意：由于上述原因，每一页返回的Rsv对象可能相同（比如一个LongTimeRsv一部分在上一次查询出现，另一部分在下一次查询）



### 管理员更改预约状态

**Des：** 供管理员审核、结束一个预约

**API：** `POST /reservation/<rsv-id>/`

**Login?:** True，且绑定，且为管理员

**请求参数：** Json Object,

| 属性 | 类型 | 说明                       |
| ---- | ---- | -------------------------- |
| op   | int  | 指明操作类型，现支持的值： |
|      |      | 1: 审核预约， 2：完成预约  |

* 当`op == 1`时，包含如下属性：

  | 属性   | 类型   | 说明           |
  | ------ | ------ | -------------- |
  | pass   | int    | 1 通过，0 拒绝 |
  | reason | string | 审核批语       |
  
* 当`op == 2`时，不需要包含其他属性



**返回值：** Json Object

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |

**错误码：** 

| code | errcode      | 说明             |
| ---- | ------------ | ---------------- |
| 201  | 未找到该预约 | 不存在这个预约   |
| 202  | 预约已开始   | 预约已经开始     |
| 203  | 预约已结束   | 预约已经完成     |
| 204  | 预约被拒绝   | 预约被审核拒绝   |
| 205  | 预约等待审核 | 预约还在等待审核 |



## 建议

### Advice 对象

包含如下属性：

| 属性      | 类型   | 说明                           |
| --------- | ------ | ------------------------------ |
| id        | int    | 这个建议的ID                   |
| proponent | string | 建议人                         |
| title     | string | 建议标题                       |
| content   | string | 建议主体，后端不关心其内容格式 |
| state     | int    | 建议状态                       |
| response  | string | 建议答复                       |

**state** 说明：

| 值   | 说明     |
| ---- | -------- |
| 1    | 等待回复 |
| 2    | 已回复   |





### 错误码说明

| code | errmsg       | 说明                  |
| ---- | ------------ | --------------------- |
| 101  | 未找到该反馈 | 找不到提供的advice-id |





### 管理员获取建议列表

**API:** `GET /advice/?state=<state>&st=<st>&ed=<ed>&p=<page>`

**Login:** True, 且绑定，且为管理员

**请求参数：**

| 参数  | 类型 | 必选 | 说明                                                    |
| ----- | ---- | ---- | ------------------------------------------------------- |
| state | int  | 否   | 根据state筛选，默认不筛选                               |
| st    | int  | 否   |                                                         |
| ed    | int  | 否   | 根据建议提交时间筛选，默认不筛选                        |
| p     | int  | 否   | 指明页数，默认1。条目可能过多，进行分页，每页20条记录。 |

**返回值：** Json Object，属性如下：

| 属性   | 类型       | 说明                              |
| ------ | ---------- | --------------------------------- |
| code   | int        | 错误码                            |
| errmsg | string     | 错误信息                          |
| page   | int        | 指明当前页数                      |
| advice | Json Array | 包含Advice对象，不包含content属性 |



### 用户提交建议

**API:** `POST /advice/`

**Login:** True，且绑定。

**请求参数：** Json Object, 属性如下：

| 属性    | 类型   | 说明     |
| ------- | ------ | -------- |
| title   | string | 建议标题 |
| content | string | 建议主体 |

**返回参数：** Json Object，

| 属性      | 类型   | 说明     |
| --------- | ------ | -------- |
| code      | int    | 错误码   |
| errmsg    | string | 错误信息 |
| advice-id | int    | 建议的id |



### 用户获取建议列表

**API：** `GET /advice/me/?state=<state>&st=<st>&ed=<ed>&p=<page>`

**Args：**

| 参数  | 类型 | 必选 | 说明                                                    |
| ----- | ---- | ---- | ------------------------------------------------------- |
| state | int  | 否   | 根据state筛选，默认不筛选                               |
| st    | int  | 否   |                                                         |
| ed    | int  | 否   | 根据建议提交时间筛选，默认不筛选                        |
| p     | int  | 否   | 指明页数，默认1。条目可能过多，进行分页，每页20条记录。 |

**返回值：** Json Object，属性如下：

| 属性   | 类型       | 说明                              |
| ------ | ---------- | --------------------------------- |
| code   | int        | 错误码                            |
| errmsg | string     | 错误信息                          |
| page   | int        | 指明当前页数                      |
| advice | Json Array | 包含Advice对象，不包含content属性 |





### 获取建议详细信息

**API:** `GET /advice/<advice-id>`

**Login:** True，且绑定

**Args：** advice-id

**返回值：**

| 属性   | 类型   | 说明             |
| ------ | ------ | ---------------- |
| code   | int    | 错误码           |
| errmsg | string | 错误信息         |
| advice | Advice | 完整的Advice对象 |



### 回复建议

**API：** `POST /advice/<advice-id>`

**Login:** True，且绑定，且为管理员

**Args:** advice-id

**请求参数：** Json Object，

| 属性     | 类型   | 说明 |
| -------- | ------ | ---- |
| response | string | 答复 |

推荐的回复方法：

* 如果是添加功能啥的，直接回复一个到github issue的链接，方便我们开发者管理。

**返回值：**

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |







## Carousel

### Carousel 对象

包含如下属性：

| 属性         | 类型             | 说明                                         |
| ------------ | ---------------- | -------------------------------------------- |
| id           | int64            | 唯一标识符                                   |
| owner        | string           | 发布这个carousel的用户                       |
| st           | int64, timestamp | 推送开始时间                                 |
| ed           | int64, timestamp | 推送结束时间                                 |
| content      | string           | 储存的相关数据，后端不关心其内容             |
|              |                  | (可以存个字符串形式的json)                   |
| hide         | int              | 是否被隐藏，一般不会返回这个字段             |
| last-version | int              | 上一个版本的id，不可修改，一般不返回此属性。 |



### 错误码说明

| code | errmsg       | 说明                    |
| ---- | ------------ | ----------------------- |
| 101  | 未找到该宣传 | 找不到提供的carousel-id |





### 获取Carousel列表

**API:** `GET /carousel/`

**Login:** False

**返回值:** Json Object，包含如下内容

| 属性      | 类型       | 说明               |
| --------- | ---------- | ------------------ |
| code      | int        | 错误码             |
| errmsg    | string     | 错误信息           |
| carousels | Json Array | Carousel对象的列表 |

注：只会返回当前处于推送时间段内（也即 st <= currentTime < ed）的Carousel。



### 添加Carousel

**API:** `POST /carousel/`

**Login:** True, 且登录，且为管理员

**请求参数：** Carousel 对象，不包含`owner`、`id`、`hide`、`last-version`属性。

**返回值** ：Json Object

| 属性   | 类型   | 说明                 |
| ------ | ------ | -------------------- |
| id     | int    | 新添加的carousel的id |
| code   | int    | 错误码               |
| errmsg | string | 错误信息             |



### 修改Carousel

**API:** `POST /carousel/<carousel-id>/`

**Login:** True,且登录，且为管理员

**请求参数:** Json Object，包含 Carousel 排除 `id` 、`last-version`外的部分属性，覆盖设置服务器中对应Carousel对应属性的值。

**返回值:** Json Object

| 属性   | 类型   | 说明                 |
| ------ | ------ | -------------------- |
| id     | int    | 修改后的carousel的id |
| code   | int    | 错误码               |
| errmsg | string | 错误信息             |



### 查看Carousel详细信息

**API:** `GET /carousel/<carouselId>/`

**Login：** TRUE，且登录，且为管理员。

**返回值：** Json Object，属性如下：

| 属性     | 类型     | 说明                                               |
| -------- | -------- | -------------------------------------------------- |
| code     | int      | 错误码                                             |
| errmsg   | string   | 错误信息                                           |
| carousel | Carousel | 这个carousel的全部信息，包括`hide`和`last-version` |

注：此时`Carousel`额外包含`owner-id`属性，为发布者的openid



### 查看历史Carousel

**API:** `GET /carousel/history/?st=<st>&ed=<ed>&hide=<hide>&last-ver=<lver>&page=<page>`

**Login:** True, 且绑定，且为管理员

**Args:** 

| 参数     | 类型                  | 含义                                 |
| -------- | --------------------- | :----------------------------------- |
| st       | int64, unix timestamp | 筛选开始时间在`st`之后的carousel     |
| ed       | int64, unix timestamp | 筛选结束时间在`ed`之前的carousel     |
| hide     | int                   | 筛选`hide`属性                       |
| last-ver | int64, Carousel ID    | 筛选上一个版本为`last-ver`的carousel |

**返回值：** Json Object，包含如下属性：

| 属性      | 类型     | 说明                                               |
| --------- | -------- | -------------------------------------------------- |
| code      | int      | 错误码                                             |
| errmsg    | string   | 错误信息                                           |
| carousels | Carousel | 这个carousel的全部信息，包括`hide`和`last-version` |





## 错误码

> GJM: 我是傻逼，一开始应该设计成没有重合的错误码的 QAQ

错误码保留\[$\infin$, 100\]，作为公共错误码；\[101, +inf) 为某个API特定错误码。





公共错误码对应一览：

| code | errmsg                    | 说明                                 |
| ---- | ------------------------- | ------------------------------------ |
| 0    | success                   | 操作成功                             |
| 1    | not logged in             | 未登录                               |
| 2    | unbound                   | 未绑定姓名、班级、学号               |
| 3    | not admin                 | 非管理员使用管理员限定API            |
| 4    | request args missing      | 请求参数缺失或遗漏                   |
| 5    | request args format error | 请求参数格式错误                     |
| 6    | request args type error   | 请求参数类型错误                     |
| 7    | request args are invalid  | 请求参数值非法                       |
| 20   | database error            | 数据库错误                           |
| -100 | bugs in server side       | 服务器出现了bug，请把顾家铭打一顿 ●\|￣\|＿ |

















 

