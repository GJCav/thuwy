

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

**Scope:** ["profile admin"]

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

**Scope:** ["profile"]

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

**Scope:** ["profile"]

**Args：** advice-id

**返回值：**

| 属性   | 类型   | 说明             |
| ------ | ------ | ---------------- |
| code   | int    | 错误码           |
| errmsg | string | 错误信息         |
| advice | Advice | 完整的Advice对象 |



### 回复建议

**API：** `POST /advice/<advice-id>`

**Scope:** ["profile admin"]

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

