#include <stdio.h>
#include <stdint.h>


// https://github.com/bminor/musl/blob/master/arch/x86_64/syscall_arch.h
static inline int64_t __syscall2(int64_t n, int64_t a1, int64_t a2)
{
    int64_t ret;
    __asm__ volatile ("syscall" : "=a"(ret) : "a"(n), "D"(a1), "S"(a2)
                      : "rcx", "r11", "memory");
    return ret;
}

static inline int64_t __syscall3(int64_t n, int64_t a1, int64_t a2, int64_t a3)
{
    int64_t ret;
    __asm__ volatile ("syscall" : "=a"(ret) : "a"(n), "D"(a1), "S"(a2),
                      "d"(a3) : "rcx", "r11", "memory");
    return ret;
}


// https://github.com/bminor/musl/blob/master/include/fcntl.h
#define O_RDONLY  0
#define O_WRONLY  1
#define O_RDWR    2


// https://github.com/bminor/musl/blob/master/arch/x86_64/bits/syscall.h.in
#define SYS_read   0
#define SYS_write  1
#define SYS_open   2


int open(const char *filename, int flags)
{
    return (int)__syscall2(SYS_open, (int64_t)filename, flags);
}

ssize_t read(int fd, void *buf, size_t count)
{
    return (ssize_t)__syscall3(SYS_read, fd, (int64_t)buf, count);
}


int main(void)
{
    int fd = open("/flag1", O_RDONLY);
    if (fd < 0) {
        fprintf(stderr, "open: %d\n", fd);
        return 1;
    }

    char buf[4096];
    ssize_t length;
    if ((length = read(fd, buf, 4096)) < 0) {
        fprintf(stderr, "read: %zd\n", length);
        return 1;
    }
    buf[length] = '\0';

    printf("flag1: %s\n", buf);
    return 0;
}
