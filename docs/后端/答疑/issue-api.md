# Issue API

## 教务答疑

> 该模块参考 GitHub Issue 设计.
>
> 置顶可通过设置 `"#top"` Tag.

| Status ( under development ) | 说明         |
| ---------------------------- | ------------ |
| `open`                       | 待回答       |
| `closed`                     | 已解决       |
| `stale`                      | 该回答已过时 |

| Visibility  | 说明                 |
| ----------- | -------------------- |
| `public`    | 已审核公开           |
| `protected` | 作者准许公开, 待审核 |
| `private`   | 作者禁止公开         |

### `Issue` 对象

| 属性               | 类型                    | 说明                                               |
| ------------------ | ----------------------- | -------------------------------------------------- |
| `id`               | `int`                   | 问题 ID                                            |
| `title`            | `string`                | 标题                                               |
| `author`           | `string`                | 作者的 `open-id`                                   |
| `date`             | `int64` ( `timestamp` ) | 发布时间                                           |
| `last_modified_at` | `int64` ( `timestamp` ) | 最近更新时间                                       |
| `status`           | `string`                | 状态, eg. `"open"`, `"closed"`, `"expired"`        |
| `visibility`       | `string`                | 可见性, eg. `"public"`, `"protected"`, `"private"` |
| `tags`             | `Json Array`            | 标签, eg. `["#top", "GPA"]`                        |
| `reply_to`         | `int`                   | 该贴所回帖的 ID                                    |
| `root_id`          | `int`                   | 最最开始的提问 Issue 的 ID ( 意会一下 )            |
| `content`          | `Json`                  | 详细内容                                           |
| `attachments`      | `Json Array`            | 附件路径 ( reserved for future use )               |
| `likes`            | `int`                   | ( reserved for future use )                        |
| `favorites`        | `int`                   | ( reserved for future use )                        |
| `liked`            | `bool`                  | ( reserved for future use )                        |
| `favorited`        | `bool`                  | ( reserved for future use )                        |

### `TagMeta` 对象

| 属性          | 类型     | 说明                       |
| ------------- | -------- | -------------------------- |
| `name`        | `string` | 名称                       |
| `description` | `string` | 详细描述 ( 大概率是 `""` ) |

### 获取 Issue 简要信息列表

**Des:** 发送筛选信息, 请求该用户可见的问答 ( 可以分页 ) 的 **简要** 信息 ( 如标题, 状态, 标签等 ), 只返回根 Issue

**Scope:** `["profile"]`

**API:** `GET /issue/?params`

**Parameters:**

| 属性         | 类型                    | 缺省值               | 说明                                                                                                         |
| ------------ | ----------------------- | -------------------- | ------------------------------------------------------------------------------------------------------------ |
| `page_size`  | `int`                   | `10`                 | 当前分页展示的数据条数, **最大** 为 10, 超过 10 将被覆盖为 10                                                |
| `page_num`   | `int`                   | `1`                  | 请求第几分页                                                                                                 |
| `keywords`   | `string`                | `""`                 | 关键词, eg. `"教务 体育;生活 教务;"` 表示 ( 教务 且 体育 ) 或 ( 生活 且 教务 ) ( reserved for future use )   |
| `sort_by`    | `string`                | `"last_modified_at"` | 排序依据, eg. `"date"`, `"id"`, `"popularity"` ( under development )                                         |
| `reply_to`   | `int`                   | `None`               | ( filter ) 所回复 Issue 的 ID                                                                                |
| `root_id`    | `int`                   | `None`               | ( filter ) 所回复 Issue 所回复的 Issue ... 所回复 Issue 的 ID                                                |
| `authors`    | `string`                | `""`                 | ( filter ) 作者 ID, 置空表示筛选所有作者 ( TODO 支持传递类似 `"teacher"` 检索所有 `"teacher"` 发布的 Issue ) |
| `tags`       | `string`                | `""`                 | ( filter ) 按 Tag 筛选, 格式同 `keywords`                                                                    |
| `visibility` | `string`                | `"all"`              | ( filter ) 根据可见性筛选, 对当前用户不可见的 `Issue` 将不会出现                                             |
| `start_time` | `int64` ( `timestamp` ) | `0`                  | ( filter ) 开始时间                                                                                          |
| `end_time`   | `int64` ( `timestamp` ) | `(2 ** 63) - 1`      | ( filter ) 结束时间                                                                                          |
|              |                         |                      | more filters under development                                                                               |

**Response:**

| 属性     | 类型         | 说明                                                                                               |
| -------- | ------------ | -------------------------------------------------------------------------------------------------- |
| `code`   | `int`        | 错误码                                                                                             |
| `errmsg` | `string`     | 错误信息                                                                                           |
| `count`  | `int`        | 单次请求返回的实际 Issues 的个数 ( 不是 `issues` 的大小, `issues` 是一页 )                         |
| `issues` | `Json Array` | 答疑列表, 包含多个 `Issue` 对象 ( for performance, 可能 **不含** `content`, `attachments` 等字段 ) |

### 获取详细答疑信息列表

**Des:** 发送答疑序号, 返回该答疑所在答疑树的 **完整** 信息

**Scope:**

```python
if issue["visibility"] == "public":
    requireScope(["profile"])
else:
    requireScope(["profile admin"]) or am_author()
```

**API:** `GET /issue/<id>/`

**Args:**

| 属性 | 类型  | 说明    |
| ---- | ----- | ------- |
| `id` | `int` | 问题 ID |

**Response:**

| 属性     | 类型         | 说明                       |
| -------- | ------------ | -------------------------- |
| `code`   | `int`        | 错误码                     |
| `errmsg` | `string`     | 错误信息                   |
| `issues` | `Json Array` | 列表格式的 **完整** 答疑树 |

**Error Code:**

| code | errmsg          | 说明             |
| ---- | --------------- | ---------------- |
| 101  | Issue not found | 未查询到 `Issue` |

### 提出新答疑

**Des:** 发送一个新提出的 Issue 的信息 ( 如标题, 内容, 附图片 ), 返回新 Issue 的序号. 普通用户尝试将 `visibility` 设为 `"public"` 时将会降为 `"protected"`.

**Scope:** `["profile"]`

**API:** `POST /issue/`

**Payload:**

| 属性          | 类型         | 缺省值     | 说明                                                          |
| ------------- | ------------ | ---------- | ------------------------------------------------------------- |
| `title`       | `string`     | `""`       | 标题                                                          |
| `tags`        | `string`     | `""`       | Tag 列表, 以半角 `';'` 分隔, 不含空白字符, eg. `"教务;体育;"` |
| `reply_to`    | `int`        | `None`     | 该 Issue 所回复的 Issue 的 ID, 若为 `None` 表示新提问         |
| `visibility`  | `string`     | `"public"` | 是否公开, eg. `"private"`                                     |
| `content`     | `Json`       | `{}`       | 详细内容                                                      |
| `attachments` | `Json Array` | `[]`       | ( reserved for future use )                                   |

**Response:**

| 属性       | 类型     | 说明                  |
| ---------- | -------- | --------------------- |
| `code`     | `int`    | 错误码                |
| `errmsg`   | `string` | 错误信息              |
| `issue_id` | `int`    | 发布成功的新 Issue ID |

### 修改问题状态

**Des:** 发送一系列参数 (包括问题序号, 问题的回答, 问题所加标签, 问答是否能被所有人看见), 返回是否修改成功. 尝试修改 `id`, `author`, `reply_to`, `root_id`, `date`, `last_modified_at` 将被忽略. 普通用户尝试将 `visibility` 设为 `"public"` 时将会降为 `"protected"`.

**Scope:**

```python
if 是作者:
  requireScope(["profile"])
else:
  requireScope(["profile dayi"], ["profile admin"])
```

**API:** `POST /issue/<id>/`

**Args:**

| 属性 | 类型  | 说明              |
| ---- | ----- | ----------------- |
| `id` | `int` | 需要修改的问题 ID |

**Payload:**

| 属性        | 类型          | 缺省值 | 说明                                                     |
| ----------- | ------------- | ------ | -------------------------------------------------------- |
| `new_issue` | `Json Object` | `{}`   | 新的 `Issue` 对象, 对于缺省的 `key`, 保留原始的 `value`. |

**Response:**

| 属性     | 类型     | 说明     |
| -------- | -------- | -------- |
| `code`   | `int`    | 错误码   |
| `errmsg` | `string` | 错误信息 |

**Error Code:**

| code | errmsg          | 说明             |
| ---- | --------------- | ---------------- |
| 101  | Issue not found | 未查询到 `Issue` |

### 删除提问

**Des:** 发送 Issue ID, 删除该 Issue, 返回是否删除成功

**Scope:**

```python
if 是作者:
  requireScope(["profile"])
else:
  requireScope(["profile teacher", "admin"])
```

**API:** `DELETE /issue/<id>/`

**Args:**

| 属性 | 类型  | 说明                |
| ---- | ----- | ------------------- |
| `id` | `int` | 需要删除的 Issue ID |

**Response:**

| 属性     | 类型     | 说明     |
| -------- | -------- | -------- |
| `code`   | `int`    | 错误码   |
| `errmsg` | `string` | 错误信息 |

### 查询所有 Tag

**Des:** 发送关键词, 查询包含该关键词的所有 Tag

**Scope:** `["profile"]`

**API:** `GET /issue/tag/?params`

**Params:**

| 属性      | 类型     | 缺省值 | 说明                         |
| --------- | -------- | ------ | ---------------------------- |
| `keyword` | `string` | `""`   | 关键词, 置空表示查询所有 Tag |

**Response:**

| 属性     | 类型         | 说明              |
| -------- | ------------ | ----------------- |
| `code`   | `int`        | 错误码            |
| `errmsg` | `string`     | 错误信息          |
| `tags`   | `Json Array` | 查询到的 Tag 名称 |

### 查询 Tag 详细信息

**Des:** 发送 Tag ID, 查询该 Tag 的详细信息

**Scope:** `["profile"]`

**API:** `GET /issue/tag/<name>/`

**Args:**

| 属性   | 类型     | 说明     |
| ------ | -------- | -------- |
| `name` | `string` | Tag 名称 |

**Response:**

| 属性       | 类型          | 说明                |
| ---------- | ------------- | ------------------- |
| `code`     | `int`         | 错误码              |
| `errmsg`   | `string`      | 错误信息            |
| `tag_meta` | `Json Object` | 详细 `TagMeta` 对象 |

**Error Code:**

| code | errmsg        | 说明           |
| ---- | ------------- | -------------- |
| 102  | Tag not found | 未查询到 `Tag` |

### 删除 Tag

**Des:** 发送 Tag 名称, 删除该 Tag

**Scope:** `["profile dayi", "profile admin"]`

**API:** `DELETE /issue/tag/<name>/`

**Args:**

| 属性   | 类型     | 说明     |
| ------ | -------- | -------- |
| `name` | `string` | Tag 名称 |

**Response:**

| 属性     | 类型     | 说明     |
| -------- | -------- | -------- |
| `code`   | `int`    | 错误码   |
| `errmsg` | `string` | 错误信息 |

**Error Code:**

| code | errmsg        | 说明           |
| ---- | ------------- | -------------- |
| 102  | Tag not found | 未查询到 `Tag` |
