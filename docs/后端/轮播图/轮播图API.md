

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

**返回值:** Json Object，包含如下内容

| 属性      | 类型       | 说明               |
| --------- | ---------- | ------------------ |
| code      | int        | 错误码             |
| errmsg    | string     | 错误信息           |
| carousels | Json Array | Carousel对象的列表 |

注：只会返回当前处于推送时间段内（也即 st <= currentTime < ed）的Carousel。



### 添加Carousel

**API:** `POST /carousel/`

**Scope:** ["profile"]

**请求参数：** Carousel 对象，不包含`owner`、`id`、`hide`、`last-version`属性。

**返回值** ：Json Object

| 属性   | 类型   | 说明                 |
| ------ | ------ | -------------------- |
| id     | int    | 新添加的carousel的id |
| code   | int    | 错误码               |
| errmsg | string | 错误信息             |



### 修改Carousel

**API:** `POST /carousel/<carousel-id>/`

**Scope:** ["profile"]

**请求参数:** Json Object，包含 Carousel 排除 `id` 、`last-version`外的部分属性，覆盖设置服务器中对应Carousel对应属性的值。

**返回值:** Json Object

| 属性   | 类型   | 说明                 |
| ------ | ------ | -------------------- |
| id     | int    | 修改后的carousel的id |
| code   | int    | 错误码               |
| errmsg | string | 错误信息             |



### 查看Carousel详细信息

**API:** `GET /carousel/<carouselId>/`

**Scope:** ["profile admin"]

**返回值：** Json Object，属性如下：

| 属性     | 类型     | 说明                                               |
| -------- | -------- | -------------------------------------------------- |
| code     | int      | 错误码                                             |
| errmsg   | string   | 错误信息                                           |
| carousel | Carousel | 这个carousel的全部信息，包括`hide`和`last-version` |

注：此时`Carousel`额外包含`owner-id`属性，为发布者的openid



### 查看历史Carousel

**API:** `GET /carousel/history/?st=<st>&ed=<ed>&hide=<hide>&last-ver=<lver>&page=<page>`

**Scope:** ["profile admin"]

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

