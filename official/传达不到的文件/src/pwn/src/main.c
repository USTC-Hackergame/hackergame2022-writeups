#define _GNU_SOURCE
#include <sys/types.h>
#include <sys/prctl.h>
#include <fcntl.h>
#include <limits.h>
#include <signal.h>
#include <sys/wait.h>
#include <stddef.h>
#include <stdbool.h>
#include <linux/audit.h>
#include <sys/syscall.h>
#include <sys/stat.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
#include <sys/ioctl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <sys/socket.h>
#include <string.h>
#include <sys/mman.h>

#define FLAG_LEN 48
#define STR(LEN) _STR(LEN)
#define _STR(LEN) #LEN

#define DEBUG 1

#ifdef DEBUG
    #define LOGPATH "/tmp/log"
    int logfd;

    #define LOG(...) do { \
        char buf[1024]; \
        int len = snprintf(buf, sizeof(buf), __VA_ARGS__); \
        write(logfd, buf, len); \
    } while (0)
#endif


extern int install_seccomp();

void sendfd(int socket, int fd) {
    struct msghdr msg = {0};
    struct cmsghdr *cmsg;
    char buf[CMSG_SPACE(sizeof(int))];
    struct iovec io = {.iov_base = "a", .iov_len = 1};
    msg.msg_iov = &io;
    msg.msg_iovlen = 1;
    msg.msg_control = buf;
    msg.msg_controllen = sizeof(buf);
    cmsg = CMSG_FIRSTHDR(&msg);
    cmsg->cmsg_level = SOL_SOCKET;
    cmsg->cmsg_type = SCM_RIGHTS;
    cmsg->cmsg_len = CMSG_LEN(sizeof(int));
    *(int *)CMSG_DATA(cmsg) = fd;
    msg.msg_controllen = cmsg->cmsg_len;
    sendmsg(socket, &msg, 0);
}

int recvfd(int socket) {
    struct msghdr msg = {0};
    struct cmsghdr *cmsg;
    char buf[CMSG_SPACE(sizeof(int))];
    char dummy[1];
    struct iovec io = {.iov_base = dummy, .iov_len = 1};
    msg.msg_iov = &io;
    msg.msg_iovlen = 1;
    msg.msg_control = buf;
    msg.msg_controllen = sizeof(buf);
    recvmsg(socket, &msg, 0);
    cmsg = CMSG_FIRSTHDR(&msg);
    return *(int *)CMSG_DATA(cmsg);
}

void watch_notification(int notify_fd) {
    struct seccomp_notif *req;
    struct seccomp_notif_resp *resp;
    struct seccomp_notif_sizes sizes;
    struct seccomp_notif_addfd addFd;
    char path[PATH_MAX];
    int proc_mem_fd;

    if (syscall(__NR_seccomp, SECCOMP_GET_NOTIF_SIZES, 0, &sizes) == -1) {
        perror("SECCOMP_GET_NOTIF_SIZES");
        exit(1);
    } 

    req = malloc(sizes.seccomp_notif);
    resp = malloc(sizes.seccomp_notif_resp);
    if (req == NULL || resp == NULL) {
        perror("malloc req or resp");
        exit(1);
    }

    while (1) {
#ifdef DEBUG
            LOG("waiting for notification\n");
#endif
        memset(req, 0, sizes.seccomp_notif);
        if (ioctl(notify_fd, SECCOMP_IOCTL_NOTIF_RECV, req) == -1) {
            perror("SECCOMP_NOTIF_RECV");
            exit(1);
            // continue;
        }
#ifdef DEBUG
            LOG("got notification\n");
#endif
        // printf("DEBUG: Got notification for PID %d, id %llx\n", req->pid, req->id);

        switch (req->data.nr) {
            case __NR_open:
                snprintf(path, sizeof(path), "/proc/%d/mem", req->pid);
                proc_mem_fd = open(path, O_RDONLY);
                if (proc_mem_fd == -1) {
                    perror("open proc mem");
                    exit(1);
                }

                if (ioctl(notify_fd, SECCOMP_IOCTL_NOTIF_ID_VALID, &req->id) == -1) {
                    perror("SECCOMP_IOCTL_NOTIF_ID_VALID");
                    exit(1);
                }

                if (lseek(proc_mem_fd, req->data.args[0], SEEK_SET) == -1) {
                    perror("lseek");
                    exit(1);
                }

                ssize_t s = read(proc_mem_fd, path, sizeof(path));
                if (s == -1) {
                    perror("read");
                    exit(1);
                } else if (s == 0) {
                    exit(1);
                }

// #ifdef DEBUG
//                 LOG("DEBUG: Read %ld bytes from %d: %s\n", s, req->pid, path);
// #endif

                close(proc_mem_fd);

                resp->id = req->id;
                resp->flags = 0;
                resp->val = strlen(path);

                if (strncmp(path, "/proc", 5) == 0 && strstr(path, ".") == NULL && strstr(path, "self") == NULL) {
                    resp->error = 0;
                    int tmpFd = syscall(__NR_open, path, req->data.args[1], req->data.args[2]);
                    if (tmpFd < 0) {
                        perror("open");
                        exit(1);
                    }
                    addFd.id = req->id;
                    addFd.flags = SECCOMP_ADDFD_FLAG_SEND;
                    addFd.srcfd = tmpFd;
                    addFd.newfd = 0;
                    addFd.newfd_flags = req->data.args[2]&O_CLOEXEC;
                    if (ioctl(notify_fd, SECCOMP_IOCTL_NOTIF_ADDFD, &addFd) == -1) {
                        close(tmpFd);
                        perror("SECCOMP_IOCTL_NOTIF_ADDFD");
                        exit(1);
                    }
#ifdef DEBUG
                    LOG("DEBUG: Allowed\n");
#endif
                } else {
                    resp->error = -EPERM;
#ifdef DEBUG
                    LOG("DEBUG: Access denied\n");
#endif
                }

                ioctl(notify_fd, SECCOMP_IOCTL_NOTIF_SEND, resp) == -1;
                break;
            default:
#ifdef DEBUG
                LOG("DEBUG: Unknown syscall %d\n", req->data.nr);
#endif
                exit(1);
        }
    }
}

void game() {
    int sp[2];
    pid_t child;

#ifdef DEBUG
    logfd = open(LOGPATH, O_WRONLY|O_CREAT|O_TRUNC, 0644);
#endif

#ifdef DEBUG
    LOG("DEBUG: Game started\n");
#endif

    if (socketpair(AF_UNIX, SOCK_STREAM, 0, sp) < 0) {
        perror("socketpair");
        exit(1);
    }
    child = fork();
    if (child < 0) {
        perror("fork");
        exit(1);
    }
    if (child == 0) {
        // tracee
#ifdef DEBUG
        LOG("DEBUG: Child pid %d\n", getpid());
#endif
        int r = prctl(PR_SET_PDEATHSIG, SIGTERM);
        if (r == -1) {
            perror("prctl");
            exit(1);
        }
        close(sp[1]);
        int notify_fd = install_seccomp();
        if (notify_fd < 0) {
            perror("install_seccomp");
            exit(1);
        }
        sendfd(sp[0], notify_fd);
        // close(notify_fd);
        close(sp[0]);
#ifdef DEBUG
        LOG("DEBUG: PlayGround\n");
#endif
        char * sc_addr = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
        if (sc_addr == MAP_FAILED) {
            perror("mmap");
            exit(1);
        }
        setreuid(1337, 1337);

        read(0, sc_addr, 0x1000);
        ((void (*)())sc_addr)();
    }
    else {
        // tracer
#ifdef DEBUG
        LOG("DEBUG: Parent pid %d\n", getpid());
#endif
        close(sp[0]);
        int notify_fd = recvfd(sp[1]);
        close(sp[1]);
#ifdef DEBUG
        LOG("DEBUG: Got notify fd %d\n", notify_fd);
#endif
        watch_notification(notify_fd);
        exit(0);
    }


}

void truefunc(void) {
    __asm__ __volatile__ (
        ".intel_syntax noprefix\n"

        "call game\n"

        "mov rdi, 0\n"
        "mov rax, 60\n"
        "syscall\n"

        ".att_syntax prefix\n"
        :
        :
        : "rdi", "rsi", "rdx", "rax", "rcx"
    );
}


char banner[] = "Give me your FLAG or I'll EXIT!\nFLAG: ";
char flag[] = "flag{ptr4ce_m3_4nd_1_w1ll_4lways_b3_th3r3_f0r_u}";
char tmp_flag[FLAG_LEN+1];

void fakefunc(void) {
    __asm__ __volatile__ (
        ".global _start\n"
        ".intel_syntax noprefix\n"
        "_start:\n"

        "mov rdi, 1\n"
        "lea rsi, [rip + banner]\n"
        "mov rdx, 38\n"
        "mov rax, 1\n"
        "syscall\n"

        "mov rdi, 0\n"
        "lea rsi, [rip + tmp_flag]\n"
        "mov rdx, " STR(FLAG_LEN) "\n"
        "add rdx, 1\n"
        "mov rax, 0\n"
        "syscall\n"

        "xor rcx, rcx\n"
        "lea rdi, [rip + flag]\n"
        "CMP_LOOP:\n"
        "mov al, byte ptr [rsi + rcx]\n"
        "cmp al, byte ptr [rdi + rcx]\n"
        "jne EXIT\n"
        "add rcx, 1\n"
        "cmp rcx, " STR(FLAG_LEN) "\n"
        "jne CMP_LOOP\n"

        "call truefunc\n"

        "EXIT:\n"
        "mov rdi, 0\n"
        "mov rax, 60\n"
        "syscall\n"

        ".att_syntax prefix\n"
        :
        :
        : "rdi", "rsi", "rdx", "rax", "rcx"
    );
}

int main()
{
    char buf[1024]; 
    return 0;
}

// chown nobody_1:nobody_1 ./test; chmod -rw ./test; chmod +s ./test