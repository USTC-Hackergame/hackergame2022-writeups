今年比去年忙很多，没什么时间做，基本上周日之后就没开过题了，~~不过居然还能留在榜上~~。WP……也没时间了，就写一个简单的吧。

## 看不见的彼方

看一遍禁止的 syscall，然后发现好像少了点东西……少了什么呢，共享内存？

然后去搜索了一下，Linux 大部分共享内存都是基于文件的，这就不太妙。但是幸运的是，Linux 还有几个 syscall，`shmget` 和 `shmat`，这俩玩意可以通过一个 key，在两个程序之间建立共享内存（没错，不需要文件）。而且更幸运的是，这两个 syscall，没 有 被 禁 用！

所以我们就直接新建一块共享内存，A 把东西写进去，B 读出来就行了。

A.c

``` c
#include <sys/shm.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main() {
    char token[65];
    FILE *f = fopen("/secret", "r");
    fscanf(f, "%s", token);

    int shmid = shmget((key_t)1017, 65, 0666 | IPC_CREAT);
    void *shm = shmat(shmid, 0, 0);
    char *shared = (char*)shm;

    strcpy(shared, token);

    sleep(8);

    return 0;
}
```


B.c

``` c
#include <sys/shm.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main() {
    sleep(2);

    int shmid = shmget((key_t)1017, 65, 0666 | IPC_CREAT);
    void *shm = shmat(shmid, 0, 0);
    char *shared = (char*)shm;

    puts(shared);

    return 0;
}
```
