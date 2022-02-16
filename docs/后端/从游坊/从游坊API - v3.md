# 从游坊API

## 从游坊管理

### Lecture对象

| 字段名         | 类型         | 说明                                |
| -------------- | ------------ | ----------------------------------- |
| lecture_id     | int          | 申请ID                              |
| user_id        | str          | 申请者的WECHAT_OPENID               |
| title          | VARCHAR(50) | 该期从游坊名称 |
| theme          | VARCHAR(50) | 该期从游坊主题 |
| state          | int          | 见txt文件                        |
| visible    | int | 是否可见。0表示不可见，1表示可见 |
| total          | int          | 总名额                              |
| first          | int          | 一志愿报名人数                      |
| second         | int          | 二志愿报名人数                      |
| third          | int          | 三志愿报名人数                      |
| subject        | VARCHAR(50)  | 该期从游坊学科                      |
| teacher        | VARCHAR(50)  | 授课老师                            |
| brief_intro    | VARCHAR(255) | 简介                                |
| detail_intro   | JSON         | 详细介绍                            |
| deadline       | BIGINT       | 报名截止时间                        |
| holding_time   | BIGINT       | 举办时间                           |

### 获取从游坊列表

**API:** `GET /lecture/?p=<page>&subject=<subject>&state=<state> `

**Scope:** ["profile"] 

**请求参数**

| 属性  | 类型 | 必填               | 说明                                       |
| ----- | ---- | ------------------ | ------------------------------------------ |
| p     | int  | 否，不填默认为1    | 分页获取，避免一次性数据过多，每页20条数据 |
| subject  | int  | 否，不填默认为全部 | 从游坊方向的标签                       |
| state | int  | 否，不填默认为全部 | 见txt文件                                  |

**返回值:** Json Object，其中包含：

| 属性          | 类型       | 说明                                                         |
| ------------- | ---------- | ------------------------------------------------------------ |
| code          | int        | 错误码                                                       |
| errmsg        | string     | 错误信息                                                     |
| lecture-count | int        | Lecture的总个数                                              |
| page          | int        | 返回的是第几页                                               |
| lectures      | Json Array | 包含` Lecture`对象，以deadline时间排序。**其中的Lecture对象不包含detail_intro属性** |

### 从游坊详细信息

**API:** `GET /lecture/<lecture-id>/`

**Scope:** ["profile"] 

**请求参数：** 

* `lecture-id`：要查询的从游坊id

**返回值：** Json Object，包含属性如下

| 属性    | 类型            | 说明        |
| ------- | --------------- | ----------- |
| code    | int             | 错误码      |
| errmsg  | string          | 错误信息    |
| lecture | Lecture, Object | Lecture对象 |

**错误码说明：**

| code | errmsg         | 说明                   |
| ---- | -------------- | ---------------------- |
| 101  | 未找到该从游坊 | 指定的lecture-id不存在 |

### 添加从游坊

**API：** `POST /lecture/`

**Scope:** ["profile congyou"] 

**请求参数：** Lecture，包含且只包含如下属性：

* title
* theme
* total
* subject
* teacher
* brief-intro
* detail-intro
* deadline
* holding_time

**返回参数：**

| 属性       | 类型             | 说明           |
| ---------- | ---------------- | -------------- |
| code       | int              | 错误码         |
| errmsg     | string           | 错误信息       |
| Lecture-id | LectureID, int64 | 添加的从游坊ID |

### 修改从游坊

**API:** `POST /lecture/<lecture-id>/`

**Scope:** ["profile congyou"]

**请求参数：** 

* **ARG：** lecture-id，从游坊id
* **Body：** Lecture，只能包含下表属性，不需要修改的属性可以省略
  * theme
  * title
  * total
  * subject
  * teacher
  * brief-intro
  * detail-intro
  * deadline
  * holding_time

**返回值：** Json Object，包含属性如下

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |

**错误码说明：**

| code | errmsg   | 说明           |
| ---- | -------- | -------------- |
| 403  | 权限不足 | 没有从游坊权限 |

### 删除从游坊

**API:**  `DELETE /lecture/<lecture-id>/`

**Scope:** ["profile congyou"] 

**请求参数：** lecture-id，从游坊id

**返回值：** Json Object，包含属性如下

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |

**错误码说明：**

| code | errmsg       | 说明                   |
| ---- | ------------ | ---------------------- |
| 101  | 未找到从游坊 | 指定的lecture-id不存在 |



## 从游坊报名

### Lecture_enrollment对象

| 字段名        | 类型    | 说明                                       |
| ------------- | ------- | ------------------------------------------ |
| enrollment_id | int     | 报名表id                                   |
| lecture_id    | int     | 报名的从游坊id                             |
| user_id       | int     | 报名者的WECHAT_OPENID                      |
| wish          | int     | 1-3表示一、二、三志愿，4表示管理员手动添加 |
| state         | int     | 见txt                                      |
| enrollment_time | BIGINT | 报名时间 |
| lecture       | Lecture | 不包括detail_intro                         |

### 报名从游坊

**API：** `POST /lecture_enrollment `

**Scope:** ["profile"]  

**请求参数：**

**Body: **Lecture_enrollment，包含且只包含如下属性：

* lecture_id
* wish

**返回参数：**

| 属性          | 类型   | 说明     |
| ------------- | ------ | -------- |
| code          | int    | 错误码   |
| errmsg        | string | 错误信息 |
| enrollment_id | int64  | 报名表id |

**错误码说明**

| code | errmsg           | 说明                           |
| ---- | ---------------- | ------------------------------ |
| 101  | 未找到从游坊     | 指定的lecture-id不存在         |
| 103  | 该从游坊不可报名 | 该从游坊的state != 1 |
| 201  | 你的一志愿不足了 | 用户用一志愿报名，但一志愿不足 |
| 202  | 你的二志愿不足了 | 用户用二志愿报名，但二志愿不足 |

### 用户获取自己报名的从游坊

**API:** `GET /lecture_enrollment/?p=<page>&subject=<subject>&state=<state>`

**Scope:** ["profile"]  

**请求参数**：

| 属性 | 类型 | 必填            | 说明                                       |
| ---- | ---- | --------------- | ------------------------------------------ |
| p    | int  | 否，不填默认为1 | 分页获取，避免一次性数据过多，每页20条数据 |
| subject  | int  | 否，不填默认为全部 | 从游坊方向的标签                       |
| state | int  | 否，不填默认为全部 | 见txt文件                                  |



**返回值:** Json Object，其中包含：

| 属性          | 类型       | 说明                                                        |
| ------------- | ---------- | ----------------------------------------------------------- |
| code          | int        | 错误码                                                      |
| errmsg        | string     | 错误信息                                                    |
| lecture-count | int        | Lecture的总个数                                             |
| page          | int        | 返回的是第几页                                              |
| enrollments   | Json Array | 包含` Lecture_enrollment`对象 |

### 修改报名的从游坊

**API:** `POST /lecture_enrollment/<lectureid>`

**Scope:** ["profile"]

**请求参数：** 

* **ARG：**

  | 属性      | 类型 | 必填 | 说明                   |
  | --------- | ---- | ---- | ---------------------- |
  | lectureid | int  | 是   | 用户想要修改的从游坊id |
  
* **Body：**Lecture_enrollment，包含且只包含如下属性：

  * wish

**返回值：** Json Object，包含属性如下

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |

**错误码说明：**

| code | errmsg           | 说明                           |
| ---- | ---------------- | ------------------------------ |
| 101  | 未找到从游坊     | 指定的lecture-id不存在         |
| 102  | 您还没有报名     | 修改者还没有报名该从游坊       |
| 103  | 该从游坊不可报名 | 该从游坊的state != 1 |
| 201  | 你的一志愿不足了 | 用户修改为一志愿，但一志愿不足 |
| 202  | 你的二志愿不足了 | 用户修改为二志愿，但二志愿不足 |

### 取消报名的从游坊

**API:** `DELETE /lecture_enrollment/<lectureid>/`

**Scope:** ["profile"]


**返回值：** Json Object，包含属性如下

| 属性   | 类型   | 说明     |
| ------ | ------ | -------- |
| code   | int    | 错误码   |
| errmsg | string | 错误信息 |

**错误码说明：**

| code | errmsg       | 说明                     |
| ---- | ------------ | ------------------------ |
| 101  | 未找到从游坊 | 指定的lecture-id不存在   |
| 102  | 您还没有报名 | 取消者还没有报名该从游坊 |




## 用户信息

### 用户查询自己剩余志愿数量

**API:** `GET /wish_remain`

**Scope:** ["profile"]


**返回值：** Json Object，包含属性如下

| 属性   | 类型   | 说明           |
| ------ | ------ | -------------- |
| code   | int    | 错误码         |
| errmsg | string | 错误信息       |
| first  | int    | 剩余一志愿数量 |
| second | int    | 剩余二志愿数量 |
