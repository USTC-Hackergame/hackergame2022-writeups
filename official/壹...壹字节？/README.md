# 壹...壹字节？

题解作者：[V1me](https://github.com/Roarcannotprogramming)

出题人、验题人、文案设计等：见 [Hackergame 2022 幕后工作人员](https://hack.lug.ustc.edu.cn/credits/)。

## 题目描述

- 题目分类：binary

- 题目分值：300

虚假的黑客用两字节写 shellcode，真正的黑客只用一个字节。

**[下载题目源代码](src/pwn/src/pwn.c)**

**[下载题目二进制文件](src/pwn/bin/chall)**

你可以在下面列出的两种方法中任选其一来连接题目：

- 点击下面的 "打开/下载题目" 按钮通过网页终端与远程交互。如果采用这种方法，在正常情况下，你不需要手动输入 token。
- 在 Linux、macOS、WSL 或 Git Bash 等本地终端中使用 `stty raw -echo; nc 202.38.93.111 10337; stty sane` 命令来连接题目。如果采用这种方法，你必须手动输入 token（复制粘贴也可）。**注意，输入的 token 不会被显示，输入结束后按 Ctrl-J 即可开始题目。**

无论采用哪种方法连接题目，启动题目均需要数秒时间，出现黑屏是正常现象，请耐心等待。

> 如果你不知道 `nc` 是什么，或者在使用上面的命令时遇到了困难，可以参考我们编写的 [萌新入门手册：如何使用 nc/ncat？](https://lug.ustc.edu.cn/planet/2019/09/how-to-use-nc/)

## 题解

这个题的考点是 mmap。[manual documentation](https://man7.org/linux/man-pages/man2/mmap.2.html) 里有这么一段：

> POSIX specifies that the system shall always zero fill any
> partial page at the end of the object and that system will never
> write any modification of the object beyond its end.  On Linux,
> when you write data to such partial page after the end of the
> object, the data stays in the page cache even after the file is
> closed and unmapped and even though the data is never written to
> the file itself, subsequent mappings may see the modified
> content.  In some cases, this could be fixed by calling msync(2)
> before the unmap takes place; however, this doesn't work on
> tmpfs(5) (for example, when using the POSIX shared memory
> interface documented in shm_overview(7)).

一个文件被 mmap 到内存后，如果文件不是恰好被映射到整数个页面，那么文件末尾的那个页面会被填充 0。如果你在这个页面上写入了数据，那么这些数据会被保留在内存中，即使你关闭了文件，即使你解除了映射，即使你没有将这些数据写回文件。这些数据会被保留在内存中，直到你再次映射这个文件，或者你调用 msync 将这些数据写回文件。

PS: 上一段话“如果文件不是恰好”后的内容由 copilot 补全，似乎语义没有问题。

所以我们可以先创建一个 shellcode 文件，并写入单字节 "\x90" (nop)。然后 mmap 这个文件到内存中，从第二个字节开始写入 shellcode。这样，10 秒钟后程序就会执行我们的 shellcode。

[exp](./src/exp.tar.gz)
