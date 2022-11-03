#include <stdio.h>
#include <stdint.h>


// https://github.com/bminor/musl/blob/master/arch/x86_64/syscall_arch.h
static inline int64_t __syscall3(int64_t n, int64_t a1, int64_t a2, int64_t a3)
{
    int64_t ret;
    __asm__ volatile ("syscall" : "=a"(ret) : "a"(n), "D"(a1), "S"(a2),
                      "d"(a3) : "rcx", "r11", "memory");
    return ret;
}

// https://github.com/bminor/musl/blob/master/arch/x86_64/bits/syscall.h.in
#define SYS_execve  59


int execve(const char *path, char *const argv[], char *const envp[])
{
    return __syscall3(SYS_execve, (int64_t)path, (int64_t)argv, (int64_t)envp);
}


int main(void)
{
    char *argv[] = {"readflag", NULL};
    char *envp[] = {NULL};

    int ret;
    if ((ret = execve("/readflag", argv, envp)) < 0) {
        fprintf(stderr, "execve: %d\n", ret);
        return 1;
    }
    // unreachable
}
