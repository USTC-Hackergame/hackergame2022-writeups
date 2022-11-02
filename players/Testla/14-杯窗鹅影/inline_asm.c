#include <stddef.h>

const char filename[] = "/readflag";
const char *arg[] = {"/readflag", NULL};
const char *envir[] = {NULL};

void main(int argc, char *argv[], char *envp[]) {
    asm(
        // https://lwn.net/Articles/604515/
        // syscall number
        // https://elixir.bootlin.com/linux/v3.14/source/arch/x86/syscalls/syscall_64.tbl
        "mov $59, %%rax;\n\t"
        // filename
        "mov %[filename], %%rdi;\n\t"
        // argv
        "mov %[arg], %%rsi;\n\t"
        // envp
        "mov %[envir], %%rdx;\n\t"
        // do syscall
        "syscall;\n\t"
        // return 0
        "mov $0, %%eax;\n\t"
        :
        : [filename] "r" (filename), [arg] "r" (arg), [envir] "r" (envir)
        : "%rax", "%rdi", "%rsi", "%rdx"
    );
}
