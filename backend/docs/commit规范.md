# Git commit 规范

我们使用如下规范：

```
<type>(<scope>): <subject>
    <say whatever you want here>
```

例如：

```
docs: 添加提交规范和暂定API
    - Add: docs/commit规范.md
    - Add: 后端API一览.md
    - Add: lh-req.png, 李晗提的需求
```



各个部分的解释：

**type**，必填，说明commit类别，备选标识如下：

* feat：添加新功能(feature)
* fix: 修复bug
* docs: 文档相关
* refactor: 重构，保证代码功能不会发生变化。包括代码风格变化、性能改善等。
* test: 增加测试用例
* sync: 这个commit只是为了通过github进行多端同步代码。



**scope**，可选，说明 commit 影响范围，我们常见的可以有如下：

* backend: 后端
* frontend: 前端
* ……，其他再说



**subject**，必填，commit 的简短描述，小于30个汉字，结尾不加标点符号。



**say whatever you want here**，可选，进一步的说明，至少空四个空格（不要用tab