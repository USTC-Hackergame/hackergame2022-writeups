/*
    for compile:
        gcc -o ../pwn/pwn pwn.c
*/

#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sched.h>
#include <signal.h>
#include <stdint.h>
#include <stdlib.h>
#include <sys/syscall.h>
#include <sys/prctl.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <errno.h>
#include <err.h>
#include <string.h>

char dirname[0x100];
int child_pid;

void remove_sandbox_dir() {
    char buf[0x100];
    if (strlen(dirname) > 0 && access(dirname, F_OK) == 0) {
        if (snprintf(buf, sizeof(buf), "rm -rf %s", dirname) > 0) {
            system(buf);
        }
    }
}

void alarm_handler(int sig) {
    kill(child_pid, SIGKILL);
}

void run_shellcode() {
    char sc_fname[0x100];
    int sc_fd;
    struct stat statbuf = { 0 };
    if (snprintf(sc_fname, sizeof(sc_fname), "%s/shellcode", dirname) < 0) {
        perror("snprintf");
        exit(0);
    }
    sc_fd = open(sc_fname, O_RDONLY);
    if (sc_fd < 0) {
        perror("open shellcode");
        exit(0);
    }
    if (fstat(sc_fd, &statbuf) < 0) {
        perror("fstat");
        exit(0);
    }
    if ((statbuf.st_mode & S_IFMT) != S_IFREG) {
        fprintf(stderr, "shellcode is not a regular file\n");
        exit(0);
    }
    if (statbuf.st_size != 1) {
        fprintf(stderr, "shellcode is too large\n");
        exit(0);
    }
    char *sc_buf = mmap(NULL, 0x1000, PROT_READ | PROT_EXEC, MAP_SHARED, sc_fd, 0); 

    ((void (*)())sc_buf)();

    printf("shellcode executed\n");
    exit(0);
}

int main(int argc, char **argv) {
    pid_t pid;
    int fd;
    uint32_t seed;
    int pipes[2] = { -1, -1 };
    char tmp_buf[0x100];

    if (argc < 2) {
        fprintf(stderr, "Usage: %s dirname\n", argv[0]);
        exit(0);
    }

    if (strcmp(argv[1], "/chall_env")) {
        fprintf(stderr, "dirname must be /chall_env\n");
        exit(0);
    }

    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);

    memcpy(dirname, argv[1], 0x40);
    dirname[0x40] = '\0';

    // breaper the zombie process
    if (prctl(PR_SET_CHILD_SUBREAPER, 1, 0, 0, 0) < 0) {
        perror("prctl");
        exit(0);
    }

    if (socketpair(AF_UNIX, SOCK_STREAM, 0, pipes) == -1) {
        perror("socketpair");
        exit(0);
    }
    unsigned long flags = CLONE_NEWUSER |
                          CLONE_NEWCGROUP |
                          CLONE_NEWIPC |
                          CLONE_NEWNET |
                          CLONE_NEWNS |
                          CLONE_NEWPID |
                          CLONE_NEWUTS;
    pid = syscall(SYS_clone, SIGCHLD | flags, NULL, NULL, NULL, 0);
    if (pid < 0) {
        perror("clone");
        exit(0);
    }
    if (pid == 0) {
        // child
        int tmp = 0;
        close(pipes[0]);
        // sync
        if (write(pipes[1], &tmp, sizeof(tmp)) != sizeof(tmp)) {
            perror("write");
            exit(0);
        }
        if (read(pipes[1], &tmp, sizeof(tmp)) != sizeof(tmp)) {
            perror("read");
            exit(0);
        }
        close(pipes[1]);

        // setsid();
        printf("Here is the shell! U have 10s to make you one-byte-man! :)\n");
        chroot(dirname);
        chdir("/");
        execl("/busybox", "busybox", "sh", NULL);
    }
    else {
        // parent
        int tmp = 0;
        child_pid = pid;
        close(pipes[1]);
        if (read(pipes[0], &tmp, sizeof(tmp)) != sizeof(tmp)) {
            perror("read");
            exit(0);
        }

        // set uid/gid mapping
        char buf[0x100];
        char path[0x100];
        int fd_tmp;
        if (snprintf(path, sizeof(path), "/proc/%d/setgroups", pid) < 0) {
            perror("snprintf");
            exit(0);
        }
        if ((fd_tmp = open(path, O_WRONLY)) < 0) {
            perror("open setgroups");
            exit(0);
        }
        if (write(fd_tmp, "deny", strlen("deny")) != strlen("deny")) {
            perror("write");
            exit(0);
        }

        if (snprintf(path, sizeof(path), "/proc/%d/gid_map", pid) < 0) {
            perror("snprintf");
            exit(0);
        }
        if (snprintf(buf, sizeof(buf), "%d %d 1", getgid(), getgid()) < 0) {
            perror("snprintf");
            exit(0);
        }
        if ((fd_tmp = open(path, O_WRONLY)) < 0) {
            perror("open gid_map");
            exit(0);
        }
        if (write(fd_tmp, buf, strlen(buf)) != strlen(buf)) {
            perror("write");
            exit(0);
        }

        if (snprintf(path, sizeof(path), "/proc/%d/uid_map", pid) < 0) {
            perror("snprintf");
            exit(0);
        }
        if (snprintf(buf, sizeof(buf), "%d %d 1", getuid(), getuid()) < 0) {
            perror("snprintf");
            exit(0);
        }
        if ((fd_tmp = open(path, O_WRONLY)) < 0) {
            perror("open uid_map");
            exit(0);
        }
        if (write(fd_tmp, buf, strlen(buf)) != strlen(buf)) {
            perror("write");
            exit(0);
        }

        // sync
        if (write(pipes[0], &tmp, sizeof(tmp)) != sizeof(tmp)) {
            perror("write");
            exit(0);
        }
        close(pipes[0]);

        // signal(SIGCHLD, child_hanler);
        signal(SIGALRM, alarm_handler);
        alarm(10);

        while (1) {
            pid_t p = waitpid(-1, NULL, __WALL);
            if (p == -1) {
                if (errno != ECHILD) {
                    perror("waitpid");
                    exit(0);
                }
                break;
            }
        }
        run_shellcode();
    }
}