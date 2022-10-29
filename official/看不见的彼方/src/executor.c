#include <seccomp.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

void add_rule(scmp_filter_ctx *ctx, int syscall) {
    int rc = seccomp_rule_add(*ctx, SCMP_ACT_ERRNO(1), syscall, 0);
    if (rc < 0) {
        printf("seccomp_rule_add failed");
        exit(1);
    }
}

int main(int argc, char **argv) {
    if (argc != 2) {
        printf("Wrong number of arguments.\n");
        exit(1);
    }
    char *program = argv[1];

    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_ALLOW);
    if (!ctx) {
        printf("seccomp_init failed");
        exit(1);
    }
    add_rule(&ctx, SCMP_SYS(socket));
    add_rule(&ctx, SCMP_SYS(accept));
    add_rule(&ctx, SCMP_SYS(bind));
    add_rule(&ctx, SCMP_SYS(connect));
    add_rule(&ctx, SCMP_SYS(listen));
    add_rule(&ctx, SCMP_SYS(recv));
    add_rule(&ctx, SCMP_SYS(recvfrom));
    add_rule(&ctx, SCMP_SYS(recvmsg));
    add_rule(&ctx, SCMP_SYS(send));
    add_rule(&ctx, SCMP_SYS(sendmsg));
    add_rule(&ctx, SCMP_SYS(sendto));
    add_rule(&ctx, SCMP_SYS(setsockopt));
    add_rule(&ctx, SCMP_SYS(shutdown));
    add_rule(&ctx, SCMP_SYS(socketcall));
    add_rule(&ctx, SCMP_SYS(socketpair));
    add_rule(&ctx, SCMP_SYS(getsockname));
    add_rule(&ctx, SCMP_SYS(getpeername));
    add_rule(&ctx, SCMP_SYS(getsockopt));
    add_rule(&ctx, SCMP_SYS(accept4));
    add_rule(&ctx, SCMP_SYS(recvmmsg));
    add_rule(&ctx, SCMP_SYS(sendmmsg));
    add_rule(&ctx, SCMP_SYS(ptrace));

    if (seccomp_load(ctx)) {
        printf("seccomp rules failed to load.\n");
        exit(1);
    }
    seccomp_release(ctx);

    execve(program, NULL, NULL);
    printf("Failed to execute program.\n");
    return 1;
}
