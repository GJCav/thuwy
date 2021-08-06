# API 约定

## 鉴权

### login

**Des:** 第一次登陆

**URL:** `/login`

**Method:** POST

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

| code    | errmsg                 | 说明                                               |
| ------- | ---------------------- | -------------------------------------------------- |
| ~~101~~ | ~~code missing~~       | ~~未将wx.login()获得的code上传到服务器或格式错误~~ |
|         |                        | 已废弃，见 code = 4 的说明                         |
| 102     | svr request timeout    | 服务器调用微信API超时                              |
| 103     | svr cnt err            | 服务器网络异常                                     |
| 201     | not 200 response       | 微信返回了非200的响应                              |
| 202     | incomplete wx response | 微信返回的数据不全                                 |
| 203     | wx reject svr          | 微信拒绝了服务器，此时有wx-\*属性                  |
| 200     | unknown error          | 服务器出现未知的异常                               |



**Set-Cookie？：**True

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



一次登陆后过多久需要重新登陆还在纠结(ー`´ー)，先不管吧。****



### bind

**Des:**  设置用户的学号、姓名、班级

**URL:** `/bind`

**Method:** POST

**Login?:** True

**请求参数:** Json Object

| 属性  | 类型   | 必填 | 说明                                |
| ----- | ------ | ---- | ----------------------------------- |
| id    | string | 是   | 学号，满足如下正则：`^\d+$`         |
| name  | string | 是   | 姓名                                |
| clazz | string | 是   | 班级，满足如下正则：`^未央-.+\d\d$` |

**返回值:** Json Object，其中包含属性：

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |

**错误码说明：**

| code | errmsg            | 说明                         |
| ---- | ----------------- | ---------------------------- |
| 101  | school id existed | 想要绑定的学号已经被绑定过了 |



### GET /profile/3

**Des：** 获取当前用户信息

**请求参数：** 无

**返回值：** Json Object，属性如下：

| 属性      | 类型   | 说明     |
| --------- | ------ | -------- |
| name      | string | 姓名     |
| clazz     | string | 班级     |
| school-id | string | 学号     |
| code      | int    | 错误码   |
| errmsg    | string | 错误信息 |



### POST /admin/

**Des:** 申请当前用户成为管理员

**URL:** `/admin/`

**Method:** POST

**Login:** True，且需要绑定

**请求参数：** 无

**返回值：** Json Object，属性如下：

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |



## 物品管理

### GET /item/

> 我们把所有能被预约的东西都称之为 `item` ，包括摄像机、29号楼房间等。

**Des:** 获取物品列表

**URL**： `/item?p=<page>/`

**Method:** GET

**Login?:**  False

**请求参数**：

| 属性 | 类型 | 必填              | 说明                                       |
| ---- | ---- | ----------------- | ------------------------------------------ |
| p    | int  | 否，不填写默认为1 | 分页获取，避免一次性数据过多，每页20条数据 |

**返回值:** Json Object，其中包含：

| 属性       | 类型       | 说明                                     |
| ---------- | ---------- | ---------------------------------------- |
| code       | int        | 错误码                                   |
| errmsg     | string     | 错误信息                                 |
| item-count | int        | item的总个数                             |
| page       | int        | 返回的是第几页                           |
| items      | Json Array | 包含`Item`对象，详见 [说明](#对象说明)， |



### POST /item/

**Des：** 添加物品

**URL：** `POST /item/`

**Method:** POST

**Login?:** True，且绑定，且是管理员

**请求参数：**Item，包含且只包含如下属性：

* name

* brief-intro
* md-intro
* thumbnail
* rsv-method

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



### GET /item/\<item-id>

**Des：** 获取物品详细信息，包括`md-intro`、`delete`属性

**Login?：** False

**请求参数：**

* `item-id`：要查询的物品id

**返回值：** Json Object，包含属性如下

| 属性   | 类型         | 说明     |
| ------ | ------------ | -------- |
| code   | int          | 错误码   |
| errmsg | string       | 错误信息 |
| item   | Item, Object | Item对象 |

**错误码说明：**

| code | errmsg            | 说明                |
| ---- | ----------------- | ------------------- |
| 101  | item id not found | 指定的item-id不存在 |



### POST /item/\<item-id>

**Des：** 修改物品信息

**Login?：** True，要求绑定、登陆

**请求参数：** 

* **URL：** item-id，物品id

* **Body：** Rsv，只能包含下表属性，不需要修改的属性可以省略
  * name
  * available
  * brief-intro
  * md-intro
  * thumbnail
  * rsv-method

**返回值：** Json Object，包含属性如下

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |

**错误码说明：**

| code | errmsg         | 说明                |
| ---- | -------------- | ------------------- |
| 101  | item not found | 指定的item-id不存在 |



### DELETE /item/\<item-id>

**Des：** 删除物品

**请求参数：** 

* **URL：** item-id，物品id

**返回值：** Json Object，包含属性如下

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |

**错误码说明：**

| code | errmsg         | 说明                |
| ---- | -------------- | ------------------- |
| 101  | item not found | 指定的item-id不存在 |



### GET /item/\<item-id>/**reservation**

**Des:** 查询某个物品未来一周的预约信息。

**URL:** `/item/<item-id>/reservation`

**Method:** GET

**Login?:** False

**请求参数：** Json Object，属性如下：

| 属性    | 类型  | 必填 | 说明           |
| ------- | ----- | ---- | -------------- |
| item-id | int64 | 是   | 要查询的物品id |

**返回值：**Json Object，属性如下：

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

### GET /reservation/\<rsv-id>

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

| code | errmsg                | 说明               |
| ---- | --------------------- | ------------------ |
| 101  | reservation not found | 没有找到对应的预约 |







### POST /reservation/

**Des:** 提交一个预约

**URL:**  `/reserve`

**Method:** POST

**Login?:** True，且需要事先绑定姓名学号。

**请求参数** ：Rsv对象，只需包含如下属性，其余省略：

| 属性     | 类型           | 说明                             |
| -------- | -------------- | -------------------------------- |
| item-id  | int64          | 要预约物品的id                   |
| reason   | string         | 预约理由                         |
| method   | RsvMethod, int | 使用的预约方法，只能有一位为1    |
| interval | any            | 描述预约时间段，格式由method决定 |

**返回值** ：Json Object，属性如下：

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |
| rsv-id | RsvId  | 预约ID   |

**错误码说明：** 

| code | errmsg                        | 说明                                        |
| ---- | ----------------------------- | ------------------------------------------- |
| 101  | time conflict                 | 预约时间冲突                                |
| 102  | reservation time out of range | 不允许预约过去的时间且不允许预约7天后的时间 |







### reservation/me

**Des:** 查询“我的”所有预约

**URL:** `/reservation/me?st=<start-time>&ed=<end-time>&state=<state>`

**Method:** GET

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

注：此时`Rsv`对线不包含`guest`属性



### ~~DELETE /reservation/\<rsv-id>~~

**Des:** 取消一个预约

**URL:** `/reservation`

**Method:** DELETE

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

| code | errcode       | 说明           |
| ---- | ------------- | -------------- |
| 101  | rsv not exist | 不存在这个预约 |
| 102  | rsv has began | 预约已经开始   |
| 103  | rsv completed | 预约已经完成   |
| 104  | rsv rejected  | 预约被审核拒绝 |
|      |               |                |



## 对象说明

### code 错误码

错误码保留\[0, 100\]，作为公共错误码；\[101, +inf) 为某个API特定错误码。

公共错误码对应一览：

| code | errmsg                    | 说明                      |
| ---- | ------------------------- | ------------------------- |
| 0    | success                   | 操作成功                  |
| 1    | not logged in             | 未登录                    |
| 2    | unbound                   | 未绑定姓名、班级、学号    |
| 3    | not admin                 | 非管理员使用管理员限定API |
| 4    | request args missing      | 请求参数缺失或遗漏        |
| 5    | request args format error | 请求参数格式错误          |
| 6    | request args type error   | 请求参数类型错误          |
| 7    | request args are invalid  | 请求参数值非法            |
| 20   | database error            | 数据库错误                |





### Item对象

Item对象是一个Json Object对象，包含如下属性：

| 属性         | 类型           | 说明                                              |
| ------------ | -------------- | ------------------------------------------------- |
| name         | string         | 名字                                              |
| id           | int64          | 设备id                                            |
| available    | bool           | 设备是否可用，如果设备被下架，为0                 |
| delete       | bool           | 是否删除设备，只在`POST /item/`且是删除操作时存在 |
| brief-intro  | string         | 简要介绍，小于50字符                              |
| md-intro     | string         | 详细介绍，只在`/item/mdintro`返回                 |
| thumbnail    | url, string    | 缩略图的url                                       |
| rsv-method   | RsvMethod      | 支持的预约方式                                    |
| ~~rsv-info~~ | ~~Json Array~~ | ~~包含`Rsv`对象~~                                 |



### Rsv对象

Rsv对象是一个Json Object，包含如下属性：

| 属性     | 类型      | 说明                             |
| -------- | --------- | -------------------------------- |
| id       | RsvId     | 这个预约的编号                   |
| item-id  | int64     | 物品ID                           |
| guest    | string    | 预约人的**名字**                 |
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

RsvState 是一个 int 对象(具体多少位再说)，每一位对应不同的含义：

| 第 n 位 | 为True时的含义                       |
| ------- | ------------------------------------ |
| 0       | ~~等待审核~~，没有必要使用，做保留位 |
| 1       | 审核结束                             |
| 2       | 审核通过；为False，被审核拒绝        |
| 3       | 用户取消订单                         |
| 4       | 预约订单完成，指预约的Item已归还     |
| 5       | 存在违规行为                         |

注：违规行为相关的API后面再添加吧。<TODO/>