# 看不见的彼方

题解作者：[taoky](https://github.com/taoky)

出题人、验题人、文案设计等：见 [Hackergame 2022 幕后工作人员](https://hack.lug.ustc.edu.cn/credits/)。

## 题目描述

- 题目分类：binary

- 题目分值：300

虽然看见的是同一片天空（指运行在同一个 kernel 上），脚踏着的是同一块土地（指使用同一个用户执行），他们之间却再也无法见到彼此——因为那名为 `chroot(2)` 的牢笼，他们再也无法相见。为了不让他们私下串通，魔王甚至用 `seccomp(2)`，把他们调用与 socket 相关的和调试相关的系统调用的权利也剥夺了去。

但即使无法看到对方所在的彼方，他们相信，他们的心意仍然是相通的。即使心处 `chroot(2)` 的牢笼，身缚 `seccomp(2)` 的锁链，他们仍然可以将自己想表达的话传达给对方。

---

你需要上传两个 x86_64 架构的 Linux 程序。为了方便描述，我们称之为 Alice 和 Bob。两个程序会在独立的 chroot 环境中运行。

在 Alice 的环境中，secret 存储在 `/secret` 中，可以直接读取，但是 Alice 的标准输出和标准错误会被直接丢弃；在 Bob 的环境中，没有 flag，但是 Bob 的标准输出和标准错误会被返回到网页中。`/secret` 的内容每次运行都会随机生成，仅当 Bob 的标准输出输出与 Alice 的 `/secret` 内容相同的情况下，你才能够获得 flag。

执行环境为 Debian 11，两个程序文件合计大小需要在 10M 以下，最长允许运行十秒。特别地，如果你看到 "Failed to execute program." 或其他类似错误，那么说明你的程序需要的运行时库可能在环境中不存在，你需要想办法在满足大小限制的前提下让你的程序能够顺利运行。

[构建环境相关的 Dockerfile 附件](files/kanata.zip)

## 题解

这道题 idea（两个不同的 chroot 下的进程互相通信）是 @zzh1996 的，我依旧负责 implementation。

---

![yrcp](assets/yrcp.jpg)

我确信，天空将你我相连。[^1]

~~虽然好像和题目正文文案不太搭~~

---

下面说正事。

`chroot(2)` 实现了文件系统层面上的隔离，但是它的文档里面这么写：

> this call changes an ingredient in the pathname resolution process and does nothing else. In particular, it is not intended to be used for any kind of security purpose, neither to fully sandbox a process nor to restrict filesystem system calls.

据我所知，在 Docker 流行之前，很多 OJ 的测评沙盒方案就是用 chroot（加上一些别的东西来做资源和 syscall 限制）。五年前，我和同学在做大一的新生研讨课课题的时候，也干过类似的事情。当然，做得好的话也还算是够用的，但是操作系统提供给进程的（共享的）资源，并不仅仅有文件系统而已。这道题希望证明的就是，即使两个进程所处的 rootfs 不同，甚至不给 `/proc/` 这种特殊的文件系统访问，它们仍然有方法可以进行 IPC（进程间通信）。对于某些特定的场合，这可能会带来侧信道的隐患。

### 容器：比 chroot 更好的隔离

作为安全性用途，`chroot(2)` 是不够的，如何更好的做轻量级的进程隔离？对于这个问题，不同的类 UNIX 操作系统给出了不同的方法，例如 FreeBSD 的方案是用 `jail(8)` 来做更严格的隔离，而 Linux 的方案则是 `namespaces(7)`：

> A namespace wraps a global system resource in an abstraction that makes it appear to the processes within the namespace that they have their own isolated instance of the global resource. Changes to the global resource are visible to other processes that are members of the namespace, but are invisible to other processes. One use of namespaces is to implement containers.

我们也可以一瞥 OS 有多少资源：

```
       Namespace Flag            Page                  Isolates
       Cgroup    CLONE_NEWCGROUP cgroup_namespaces(7)  Cgroup root directory
       IPC       CLONE_NEWIPC    ipc_namespaces(7)     System V IPC, POSIX
                                                       message queues
       Network   CLONE_NEWNET    network_namespaces(7) Network devices, stacks,
                                                       ports, etc.
       Mount     CLONE_NEWNS     mount_namespaces(7)   Mount points
       PID       CLONE_NEWPID    pid_namespaces(7)     Process IDs
       Time      CLONE_NEWTIME   time_namespaces(7)    Boot and monotonic clocks
       User      CLONE_NEWUSER   user_namespaces(7)    User and group IDs
       UTS       CLONE_NEWUTS    uts_namespaces(7)     Hostname and NIS domain
                                                       name
```

除了文件系统（`CLONE_NEWNS`）以外，还有很多资源是进程之间共享的，比如说 IPC（`CLONE_NEWIPC`）和 PID（`CLONE_NEWPID`）。

因为 PID 没有隔离，所以（相同用户的）进程之间可以用信号来互相通信。本题解会给出使用**信号**机制的解法。当然，这道题目解法是开放的，所以很可能有更多有意思的解法。

### 信号 101

信号可能是作为普通 Unix-like 用户最常使用的 IPC 工具：当我们在终端中按下 Ctrl + C，想关掉一个程序时，对应给程序的信号就是 `SIGINT`；程序出现内存访问问题，「段错误」崩溃的时候，它收到的信号就是 `SIGSEGV`；我们想无论如何杀死一个进程，用 `kill -9` 的时候，给程序的信号就是 `SIGKILL`。关于信号，`signal(7)` 中有详细的介绍。

我们可以用命令行工具 `kill(1)` 向进程发送指定的信号：

```console
$ kill -SIGUSR2 12345
```

在编程实现的时候，我们可以用 `kill(2)` 发送信号：

```c
#include <signal.h>

int main(void) {
    kill(12345, SIGUSR2);  // error handling omitted
    return 0;
}
```

（并且从 `kill(2)` 的文档，我们可以知道，特权进程可以发信号，相同用户之间的进程也可以互相发信号）

而进程怎么处理收到的信号呢？最简单的方法是用 `signal(2)`（这是 ANSI C 的标准库函数），不过文档里面也写了：

> WARNING: the behavior of signal() varies across UNIX versions, and has also varied historically across different versions of Linux. Avoid its use: use sigaction(2) instead.

所以下面的例子都用 `sigaction(2)`。

```c
#include <signal.h>
#include <stdio.h>
#include <unistd.h>

void handler(int signo, siginfo_t *info, void *context) {
    // According to signal-safety(7)
    // printf(), putchar(), etc. is not safe to use in signal handler
    char msg[] = "I'm exiting now!\n";
    write(STDOUT_FILENO, msg, sizeof(msg));
    _exit(0);  // Well exit() is also not safe...
}

int main(void) {
    printf("My PID: %d\n", getpid());

    struct sigaction act = { 0 };
    act.sa_sigaction = &handler;
    sigaction(SIGUSR2, &act, NULL);

    sleep(3600);

    return 0;
}
```

可以跑一下验证：

```console
$ ./a.out &
My PID: 1597202
$ kill -SIGUSR2 1597202
I'm exiting now!
$ jobs
[1]+  Done                    ./a.out
```

既然我们现在已经有了工具，那么就差实现了。

### 使用信号

Alice 和 Bob 间要使用信号沟通，首先需要知道对方的 PID。坏消息是，我们的环境里面没有 `/proc`，没法直接遍历来得到 PID；好消息是，题目环境在容器里面运行，我们提交的程序的 PID 都很小（这一点也可以自己 `getpid()` 验证），所以完全可以小范围枚举。

这一阶段的 protocol 如下：Alice 向 PID 2 - 19 的进程发送信号，Bob 收到对应信号后记录 Alice 的 PID 并向发送信号的 PID 返回信号。Alice 收到返回的信号后也记录 Bob 的 PID。

这里，发送信号人的 PID 的信息在 handler 的 `siginfo_t *info` 里面（`info->si_pid`，需要设置 `SA_SIGINFO` 这个 flag 来让 handler 接受三个参数）。让我们来试一下：

Alice:

```c
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

// async-signal safe variable type
volatile sig_atomic_t receiver = -1;

void handler(int signo, siginfo_t *info, void *context) {
    receiver = info->si_pid;
}

int main(void) {
    // sleep a while for Bob to be ready
    sleep(1);
    int pid = getpid();
    struct sigaction sa;
    sa.sa_sigaction = handler;
    sa.sa_flags = SA_SIGINFO;  // required if we use siginfo_t *info
    if (sigaction(SIGUSR2, &sa, NULL) == -1) {
        perror("sigaction");
        exit(-1);
    }
    for (int i = 2; i < 20; i++) {
        if (i == pid) {
            // don't send signal to myself
            continue;
        }
        int _ = kill(i, SIGUSR2);
        if (_) {
            printf("sending sig to %d failed", i);
            perror("kill");
        }
    }
    return 0;
}
```

Bob:

```c
#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <stdlib.h>

void handler(int signo, siginfo_t *info, void *context) {
    char buf[4] = {};
    kill(info->si_pid, SIGUSR2);
    buf[0] = info->si_pid / 10 + '0';
    buf[1] = info->si_pid % 10 + '0';
    buf[2] = '\n';
    write(STDERR_FILENO, buf, 3);
    _exit(0);
}

int main(void) {
    fprintf(stderr, "%d\n", getpid());
    struct sigaction sa;
    sa.sa_sigaction = handler;
    sa.sa_flags = SA_SIGINFO;
    if (sigaction(SIGUSR2, &sa, NULL) == -1) {
        perror("sigaction");
    }
    sleep(5);
    return 0;
}
```

验证可以得到 Bob 成功获得了 Alice 的 PID。接下来就可以传递 secret 了。可能有人会问：信号还能居然带数据发送吗？答案是可以的：`siginfo_t` 这个结构体里面有这个元素：

```c
union sigval si_value; /* Signal value */
```

普通的 `kill(2)` 当然无法承载更多的信息，我们可以读一下 `signal(7)` 看看哪些系统调用可以让我们发带 `si_value` 的信号：

```
Sending a signal
    The following system calls and library functions allow the caller to send a signal:

    raise(3)
            Sends a signal to the calling thread.

    kill(2)
            Sends  a signal to a specified process, to all members of a specified process group, or to all processes on the sys‐
            tem.

    pidfd_send_signal(2)
            Sends a signal to a process identified by a PID file descriptor.

    killpg(3)
            Sends a signal to all of the members of a specified process group.

    pthread_kill(3)
            Sends a signal to a specified POSIX thread in the same process as the caller.

    tgkill(2)
            Sends a signal to a specified thread within a specific  process.   (This  is  the  system  call  used  to  implement
            pthread_kill(3).)

    sigqueue(3)
            Sends a real-time signal with accompanying data to a specified process.
```

读过一遍上面几个系统调用的文档之后可以发现，只有 `pidfd_send_signal(2)` 和 `sigqueue(3)` 可以让我们自由发挥，而其中 `pidfd_send_signal(2)` 我们似乎无法轻松构造对应的 pidfd，所以就只剩 `sigqueue(3)` 了。

看起来好像不难用：

```c
int sigqueue(pid_t pid, int sig, const union sigval value);
```

并且可以知道：

```c
union sigval {
    int   sival_int;
    void *sival_ptr;
};
```

让我们试试看用之前测试信号的例子：

receiver:

```c
#include <signal.h>
#include <stdio.h>
#include <unistd.h>

void handler(int signo, siginfo_t *info, void *context) {
    // According to signal-safety(7)
    // printf(), putchar(), etc. is not safe to use in signal handler
    char msg[] = "Received: ";
    write(STDOUT_FILENO, msg, sizeof(msg));
    unsigned char chr = (unsigned char)(info->si_value.sival_int);
    write(STDOUT_FILENO, &chr, 1);
    _exit(0);  // Well exit() is also not safe...
}

int main(void) {
    printf("My PID: %d\n", getpid());

    struct sigaction act = { 0 };
    act.sa_sigaction = &handler;
    act.sa_flags = SA_SIGINFO;
    sigaction(SIGUSR2, &act, NULL);

    sleep(3600);

    return 0;
}
```

sender:

```c
#include <signal.h>
#include <stdio.h>
#include <unistd.h>

int main(void) {
    int pid;
    scanf("%d", &pid);
    union sigval value;
    value.sival_int = (int)'x';
    int _ = sigqueue(pid, SIGUSR2, value);
    if (_ == -1)
        perror("sigqueue");
    return 0;
}
```

测试一下：

```console
$ ./receiver &
My PID: 1662675
$ ./sender
1662675
Received: x[1]+  Done                    ./receiver
```

可以看到字节 `'x'` 成功从 sender 传递到了 receiver。按照这个思路，可以有两种不同的 protocol：

- receiver 从 sender 收到数据后返回 ACK 信号，receiver 接收到 ACK 后再发送下一个数据
- 或者，receiver 仅仅输出 sender 发送的内容，sender 自己控制发送信号的频率

这里选择后者实现（可以少写一点处理 ACK 的代码），一个实现如下：

Alice:

```c
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

volatile sig_atomic_t receiver = -1;

void handler(int signo, siginfo_t *info, void *context) {
    receiver = info->si_pid;
}

int main(void) {
    // sleep a while for Bob to be ready
    sleep(1);
    int pid = getpid();
    struct sigaction sa;
    sa.sa_sigaction = handler;
    sa.sa_flags = SA_SIGINFO;
    if (sigaction(SIGUSR2, &sa, NULL) == -1) {
        perror("sigaction");
        exit(-1);
    }
    for (int i = 2; i < 20; i++) {
        if (i == pid) {
            // don't send signal to myself
            continue;
        }
        int _ = kill(i, SIGUSR2);
        if (_) {
            printf("sending sig to %d failed", i);
            perror("kill");
        }
    }
    while (receiver == -1);

    FILE *f = fopen("/secret", "r");
    char buf[5000] = {};
    fgets(buf, 5000, f);
    // send data to receiver
    for (int i = 0; buf[i] != '\0'; i++) {
        union sigval value;
        value.sival_int = (int)buf[i];
        sigqueue(receiver, SIGUSR2, value);
        usleep(10);
    }
    fclose(f);
    return 0;
}
```

Bob:

```c
#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <stdlib.h>

void handler(int signo, siginfo_t *info, void *context) {
    unsigned char x = (int)(info->si_value.sival_int);
    if (x == 0) {
        char buf[4] = {};
        kill(info->si_pid, SIGUSR2);
        buf[0] = info->si_pid / 10 + '0';
        buf[1] = info->si_pid % 10 + '0';
        buf[2] = '\n';
        write(STDERR_FILENO, buf, 3);
        // _exit(0);
    } else {
        write(STDOUT_FILENO, &x, 1);
    }
}

int main(void) {
    fprintf(stderr, "%d\n", getpid());
    struct sigaction sa;
    sa.sa_sigaction = handler;
    sa.sa_flags = SA_SIGINFO;
    if (sigaction(SIGUSR2, &sa, NULL) == -1) {
        perror("sigaction");
    }
    while (1) {
        // wrap sleep() with loop, otherwise sleep() exits ahead of time when getting signal
        sleep(5);
    }
    return 0;
}
```

### 更好的方案

以上的代码，大部分情况下已经可以拿到 flag 了，但是有一个潜在的问题：如何确认 `usleep()` 的时长是恰当的？

如果两次发送期间时间太短，上一个信号事件还没处理，那么就会导致上一个事件的信号被覆盖掉（"Standard signals do not queue."）。如果我们把 `usleep()` 去掉的话，就能观测到这样的问题：

```
验证失败。预期值为 3be6763437f377147abb6dfa56c282c96437bb01d92af13099cbcff77393e995
A 中的 /secret 每次执行都会重新生成，请再接再厉。

stdout (原始标准输出，前 8192 个字节，以 Python bytes 格式显示):
b'36437f37714f56c94319209ff7e95'
stderr (原始标准错误，前 8192 个字节，以 Python bytes 格式显示):
b'9\n08\n'
```

对于这样的场景，更好的解决方法是使用 POSIX 实时信号（real-time signals）。Real-time signals 好处都有啥？`signal(7)` 对此有介绍：

> Real-time signals are distinguished by the following:
>
> 1.  Multiple  instances  of  real-time signals can be queued.  By contrast, if multiple instances of a standard signal are delivered while that signal is currently blocked, then only one instance is queued.
>
> 2.  If the signal is sent using sigqueue(3), an accompanying value (either an integer or a pointer) can be sent with the signal.  If the receiving process establishes a handler for this signal using the  SA_SIGINFO  flag  to  sigaction(2), then it can obtain this data via the si_value field of the siginfo_t structure passed as the second argument to the handler.  Furthermore, the si_pid and si_uid fields of this structure can be used to obtain the PID and real user ID of the process sending the signal.
>
> 3.  Real-time signals are delivered in a guaranteed order.  Multiple real-time signals of the same type are delivered in the order they were sent.  If different  real-time  signals  are  sent  to  a process,  they  are delivered starting with the lowest-numbered signal.  (I.e., low-numbered signals have highest priority.)  By contrast, if multiple standard signals are pending for a process, the order in which they are delivered is unspecified.

我们可以尝试将 `SIGUSR2` 换成 `SIGRTMIN`，然后再试试，可以发现，不再需要 `usleep(3)` 来手动空出时间了：OS 帮我们做好了实时信号通信的维护操作。

有人可能会问：那这个信号队列是无限长的吗？答案不是，但是 POSIX 标准要求至少能塞下 32 个信号，Linux 下则有一个用户级别的限制：

> According  to POSIX, an implementation should permit at least _POSIX_SIGQUEUE_MAX (32) real-time signals to be queued to a process.  However, Linux does things differently.  In kernels up to and including 2.6.7, Linux imposes a system-wide limit on the number of queued real-time signals for all processes.  This limit can be viewed and (with  privilege)  changed  via  the  /proc/sys/kernel/rt‐sig-max  file.   A  related  file,  /proc/sys/kernel/rtsig-nr,  can  be used to find out how many real-time signals are currently queued.  In Linux 2.6.8, these /proc interfaces were replaced by the RLIMIT_SIGPENDING resource limit, which specifies a per-user limit for queued signals; see setrlimit(2) for further details.

在我的笔记本上，用户可以排队的信号的数量为：

```console
> ulimit -i
191392
```

所以应该是够的。如果担心的话，`sigqueue()` 那里加个根据返回值和 `errno` 来重试的逻辑即可。

### 出题思路

本节作者：[zzh1996](https://github.com/zzh1996)

这道题的出题思路是我提供的。

这道题想想就比较好玩。我喜欢给 Hackergame 出一些比较开放的题目，然后收集选手题解的时候可以看到很多很多有趣的不同解法，可以学到许多。

### 附注

[^1]: 原句为「きっと、そらでつながってる」，为动画《摇曳露营》的[宣传语之一](https://yurucamp.jp/news/information/5583)，和上面（第五集的）截图的剧情和氛围是相呼应的。题目文案是我当时拍脑袋想的，但是在写 writeup 的时候看到了[（不太准确的）这句话的翻译](https://bgm.tv/ep/762294)，然后我当时想，一定要把这句话写在 writeup 里面，于是就变成了你现在看到的样子。这里也感谢 [Elsa Granger](https://github.com/zeyugao) 就这句话帮我做了 fact check。
