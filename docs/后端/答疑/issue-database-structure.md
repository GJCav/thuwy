# Issue Database Structure

## 答疑表

表名: `issue`

| 字段名             | 类型                                                                | 说明                                                      |
| ------------------ | ------------------------------------------------------------------- | --------------------------------------------------------- |
| `id `              | `SNOWFLAKE_ID`                                                      | 答疑 ID                                                   |
| `delete`           | `Boolean`                                                           | 是否移入回收站                                            |
| `title`            | `VARCHAR(80)`                                                       | 标题                                                      |
| `author`           | `WECHAT_OPENID`                                                     | 作者的 `open-id`                                          |
| `date`             | `BIGINT`                                                            | 发布时间                                                  |
| `last_modified_at` | `BIGINT`                                                            | 最后修改时间                                              |
| `reply_to`         | `SNOWFLAKE_ID`                                                      | 该 Issue 回复的 Issue 的 ID                               |
| `root_id`          | `SNOWFLAKE_ID`                                                      | 该 Issue 回复的 Issue 回复的 Issue ... 回复的 Issue 的 ID |
| `tags`             | `relationship(IssueTagMeta, secondary=qaq_tag, backref=qaqs)`       | 标签, eg. `["#Top", "#visibility:user_public", "GPA"]`    |
| `content`          | `JSON`                                                              | 详细内容                                                  |
| `attachments`      | `Array(VARCHAR(1024))`                                              | 附件路径 (reserved for future use)                        |
| `likes`            | `relationship(User, secondary=qaq_like, backref=qaq_likes)`         | 点赞 ( reserved for future use )                          |
| `favorites`        | `relationship(User, secondary=qaq_favorite, backref=qaq_favorites)` | 收藏 ( reserved for future use )                          |

## Tag 表

表名: `issue_tag`

| 字段名     | 类型                                          | 说明    |
| ---------- | --------------------------------------------- | ------- |
| `issue_id` | `SNOWFLAKE_ID, ForeignKey(issue.id)`          | 答疑 ID |
| `tag_id`   | `SNOWFLAKE_ID, ForeignKey(issue_tag_meta.id)` | Tag ID  |

## Tag 详情表

> 以 `"#"` 开头的 Tag 为特殊标记, 如 `"#top"`, `"#status:open"` , `""#visibility:user_public"`, 一些特殊标记将不会作为 tags 在 API 中返回

表名: `issue_tag_meta`

| 字段名        | 类型                                    | 说明                    |
| ------------- | --------------------------------------- | ----------------------- |
| `name`        | `VARCHAR(80)`                           | Tag 名                  |
| `delete`      | `Boolean`                               | 是否移入回收站          |
| `description` | `Text`                                  | 简介                    |
| `issues`      | `backref to Issue, secondary=issue_tag` | 该 Tag 下的 Issues 列表 |
