---
title: Hackergame 2022 WriteUp
date: 2022-10-29 13:00:00
---

# HackerGame 2022 题解

> 朋友给我转了活动结束公布的答案，所以花了10分钟写了个 LaTeX3 的解法。

## LaTeX 机器人

LaTeX 对于字符的映射采用类别码机制，所以为了把特殊字符看作正常字母，需要使用一些混沌邪恶的类别码操作。这个思路类似于 LaTeX2e 提供的 `\makeatother` 宏，在其他同学的题解中有所体现。

当然，因为本人恰好搞过一些宏包开发，所以熟悉封装更完善的 [LaTeX3](http://mirrors.ctan.org/macros/latex/contrib/l3kernel/interface3.pdf) 编程接口。其中的 `str` 数据类型可以将输入的类别码漂白，形成可供直接使用的字符串。

所以解答就是开启 LaTeX3 语法，读取文件到临时变量，转换成字符串输出。当然，不用 `$$` 退出数学模式也能得到正确结果，只不过字母会显示为斜体。

```
$$ \ExplSyntaxOn \file_get:nnN {/flag2} { } \l_tmpa_tl \tl_to_str:N \l_tmpa_tl $$
```

对应的最小工作示例为
```latex
\documentclass{article}
\begin{document}
  \ExplSyntaxOn
  \file_get:nnN {/flag2} { } \l_tmpa_tl
  \tl_to_str:N \l_tmpa_tl
  % \ExplSyntaxOff
\end{document}
```