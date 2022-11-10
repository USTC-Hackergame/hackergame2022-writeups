# HeiLang

题解作者：[volltin](https://github.com/volltin)

出题人、验题人、文案设计等：见 [Hackergame 2022 幕后工作人员](https://hack.lug.ustc.edu.cn/credits/)。

## 题目描述

- 题目分类：general

- 题目分值：100

来自 Heicore 社区的新一代编程语言 HeiLang，基于第三代大蟒蛇语言，但是抛弃了原有的难以理解的 `|` 运算，升级为了更加先进的语法，用 `A[x | y | z] = t` 来表示之前复杂的 `A[x] = t; A[y] = t; A[z] = t`。

作为一个编程爱好者，我觉得实在是太酷了，很符合我对未来编程语言的想象，科技并带着趣味。

## 题解

这道题目只需要把 [附件](src/getflag.hei.py) 中的新一代编程语言改回现有的落后的编程语言理解的形式即可。

### 解法一：文本替换

把附件中的 `|` 替换成 `] = a[`（这一步可以用编辑器的查找替换功能实现），就可以得到标准的 Python 脚本了，运行即可得到 flag。

参考：
```python
a[1 | 2 | 3] = 4

# replace(" | ", "] = a["))

a[1] = a[2] = a[3] = 4
```

### 解法二：编写新的解析器

既然是一门新的编程语言，那么就可以自己实现一个新的解释器 / 编译器，不过这个对于解出这道题可能过于复杂了，好在现在已经有一个类似的开源项目实现了这种先进的语法，可以直接参考 [kifuan](https://github.com/kifuan) 的 [helang](https://github.com/kifuan/helang) 来解析并且执行 HeiLang。
