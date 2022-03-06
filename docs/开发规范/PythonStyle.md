# Python 风格规范

> 本文档大量参考了[Google Style Guide for Python](https://google.github.io/styleguide/pyguide.html), 但也有所修改。本文中所有未说明事项以Google的文档为准。
>
> by GJM, 20220125



## Language Rules

### 小心Lexical Scoping

详见：https://google.github.io/styleguide/pyguide.html#216-lexical-scoping

请谨慎使用。



### 类型注解

对于绑定到路由的函数及其函数参数不需要注解。

局部变量可以不具备注解，但若该变量类型是一个具有很多方法的类，推荐使用注解，方便vscode给出代码提示。

对于公共函数，函数返回值必须具有注解，函数参数推荐使用注解。

可根据自己喜好决定是否开启代码静态检查。



## Python Style Rules

### 分号结尾

不要使用分号结尾



### 使用圆括号合并多行代码

详见：https://google.github.io/styleguide/pyguide.html#32-line-length

注：原来的代码中我（顾家铭）错误的使用了很多`\`来合并多行代码，这些遗留问题会得到逐步解决。



### 缩进

规定：使用4个空格进行缩进，禁止使用制表符缩进。



### 注释与文档

#### doc string

简单了解python docstrings的编写方法，但不对文档格式进行非常严格的要求，但推荐使用[Google Style](https://google.github.io/styleguide/pyguide.html#383-functions-and-methods)，包含`Args`、`Returns/Yields`、`Raises`三个部分。

#### 函数

除非一个函数满足如下条件，否则需要编写文档：

* 外部不可见
* 非常短
* “显然“，函数名能完全表明函数的行为

#### 注释

`#`之后空一格再写注释，不然太丑了。

```
YES: # comments, comments
NO:  #comments, comments
```

#### 语言

中文、英文都可，但一定使用UTF-8编码你的代码。



### 字符串常量

多行字符串注意缩进统一，例：

```python
No:
  long_string = """This is pretty ugly.
Don't do this.
"""
Yes:
  long_string = """This is fine if your use case can accept
      extraneous leading spaces."""
Yes:
  long_string = ("And this is fine if you cannot accept\n" +
                 "extraneous leading spaces.")
Yes:
  long_string = ("And this too is fine if you cannot accept\n"
                 "extraneous leading spaces.")
```



### Stateful Resources

使用`with`处理那些需要显式释放资源的对象，例如：

```python
with open("hello.txt") as hello_file:
    for line in hello_file:
        print(line)
```



### import位置与顺序

由于flask框架下代码有一些复杂的加载逻辑，不要求所有`import`都出现在文件顶部，可以根据实际情况决定`import`的位置。

要求相关联的`import`放在一组，组与组间用空行分隔。



### 命名规范

#### 避免如下情况

* 在一个函数的开头把所有变量全部声明一遍
* 变量中出现`-`符号
* 用拼音拼写的变量名

#### 约定

| 类型                       | Public             | Internal                  |
| -------------------------- | ------------------ | ------------------------- |
| Packages                   | `lower_with_under` |                           |
| Modules                    | `lower_with_under` | `_lower_with_under`       |
| Classes                    | `CapWords`         | `_CapWords`               |
| Exceptions                 | `CapWords`         |                           |
| Functions                  | `capWords()`       | `_capWords()`             |
| Global/Class Constants     | `CAPS_WITH_UNDER`  | `_CAPS_WITH_UNDER`        |
| Global/Class Variables     | `capWords`         | `_capWords` (protected)   |
| Instance Variables         | `capWords`         | `_capWords` (protected)   |
| Method Names               | `capWords()`       | `_capWords()` (protected) |
| Function/Method Parameters | `capWords`         |                           |
| Local Variables            | `capWords`         |                           |

注：

* `CapWords`表示首字母大写的驼峰命名法
* `capWords`表示首字母小写的驼峰命名法

> Google Style Guide for Python 中大量推荐了`lower_with_under`的命名方法，但由于我原来写Java和C#较多，习惯了`capWords`的命名方法，已有的大量代码也是这么编写的，所以对Google Style Guide 有所修改。原有代码中也可能出现一些不符约定的命名，会慢慢修正。



## Formatter 

我们使用`BLACK`进行自动格式化。

为什么使用`BLACK`？因为懒得配置。

