# 传达不到的文件

题解作者：[V1me](https://github.com/Roarcannotprogramming)

出题人、验题人、文案设计等：见 [Hackergame 2022 幕后工作人员](https://hack.lug.ustc.edu.cn/credits/)。

## 题目描述

- 题目分类：binary

- 题目分值：读不到（250）+ 打不开（300）

为什么会变成这样呢？第一次有了 `04111` 权限的可执行文件，有了 `0400` 权限的 flag 文件，两份快乐的事情重合在一起；而这两份快乐，又给我带来更多的快乐。得到的，本该是……（被打死）

---

探索虚拟环境，拿到两个 flag：flag1 在 `/chall` 中，flag2 在 `/flag2` 中。

你可以在下面列出的两种方法中任选其一来连接题目：

- 点击下面的 "打开/下载题目" 按钮通过网页终端与远程交互。如果采用这种方法，在正常情况下，你不需要手动输入 token。
- 在 Linux、macOS、WSL 或 Git Bash 等本地终端中使用 `stty raw -echo; nc 202.38.93.111 10338; stty sane` 命令来连接题目。如果采用这种方法，你必须手动输入 token（复制粘贴也可）。**注意，输入的 token 不会被显示，输入结束后按 Ctrl-J 即可开始题目。**

无论采用哪种方法连接题目，启动题目均需要数秒时间，出现黑屏是正常现象，请耐心等待。

> 如果你不知道 `nc` 是什么，或者在使用上面的命令时遇到了困难，可以参考我们编写的 [萌新入门手册：如何使用 nc/ncat？](https://lug.ustc.edu.cn/planet/2019/09/how-to-use-nc/)

## 道歉

首先我为这题的检查疏忽导致的非预期道歉。由于我在验题和打包时候的疏忽导致了以下两个非预期：

1. 我在打包时忘记使用 root 用户，导致 /sbin 内的文件的 owner 是 1000，所以在 /sbin 内的文件是可以被任意更改的；
2. flag2 的权限设置错误。flag2 的 owner 应该为 0:1337，权限应该为 0440，这导致 shellcode 可以直接修改 flag2 的权限.

红豆泥私密马赛！

## 题解

### 读不到

这个题的预期解法是使用 ptrace 单步执行程序，并提取每一步的寄存器，从而理解程序逻辑。之后在 `syscall` 之前修改 `rax`（系统调用编号）为 1 (`write`)，从而泄露整个二进制文件。

[exp](./src/payload/exp_1.c)

### 打不开

通过分析第一问泄露出的二进制程序，发现和 `open` 相关的几个 syscall 都被禁止了，独独留下了一个 `open`。但是这个 open 也是有限制的，只能打开以 "/proc" 开头、不包含 "." 和 "self" 的路径。由于程序会打印 log 到 "/tmp/log"，所以我们可以通过读 log 得到自己的 PID。

题目的预期考点是 `open_tree` 这个 syscall，这个 syscall 极少被用到。它能做到以 flag `O_PATH` 打开一个路径（但是以 `O_PATH` 打开的文件/目录不能被 read/write）。所以可以先通过 `open_tree()` 打开 /flag2，之后通过 `open()` 正常打开 `/proc/<pid>/fd/<fd>`，这样就能读到 flag2。

[exp](./src/payload/exp_2.go)

再次抱歉！
