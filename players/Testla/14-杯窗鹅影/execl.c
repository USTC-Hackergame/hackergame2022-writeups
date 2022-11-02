#include "error_functions.h"

// #include <process.h>
#include <stdio.h>
#include <unistd.h>

void printcwd() {
    char wd[4096];
    if (getcwd(wd, sizeof(wd)) == NULL) {
        errExit("getcwd");
    }
    puts(wd);
}

int main(int argc, char *argv[]) {
    // const char *path = (argc == 1) ? "/readflag" : argv[1];
    // const char *path = "/readflag";

    // for (int i = 0; i < argc; ++i) {
    //     puts(argv[i]);
    // }
    // \\?\unix\dev\shm\a.exe

    // FILE *f;
    // f = fopen("/readflag", "r");
    // if (f == NULL) {
    //     perror("fopen /readflag");
    //     // No error printed
    // }
    // int c;
    // while ((c = fgetc(f)) != EOF) {
    //     printf("%02X", c);
    // }
    // puts("\ndone");
    // f = fopen("/flag2", "r");
    // if (f == NULL) {
    //     perror("fopen /flag2");
    // }
    // fopen /flag2: Permission denied

    // https://faq.cprogramming.com/cgi-bin/smartfaq.cgi?answer=1044654269&id=1043284392
    // https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/spawnlp?view=msvc-170
    // https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/spawnlp-wspawnlp?view=msvc-170
    // puts("Going to spawn");
    // _spawnlp(P_OVERLAY, path, path, NULL);
    // puts("Still running?");
    // perror("spawn failed");
    // spawn failed: No such file or directory

    // execlp(path, path, (char *)NULL);
    // errExit("execlp");
    // ERROR [ENOENT No such file or directory] execlp
    // man execve doesn't contain ENOENT
    // puts("Still running?");

    puts("Before chdir");
    printcwd();
    // On local computer
    // Z:\tmp\wine
    // On judge
    // unix
    if (chdir("/") == -1) {
        errExit("chdir");
    }
    puts("After chdir");
    printcwd();
    // On local computer
    // Z:\
    // On judge
    // unix

    // FILE *f;
    // f = fopen("readflag", "r");
    // if (f == NULL) {
    //     perror("fopen readflag");
    //     // No error printed
    // }
    // int c;
    // while ((c = fgetc(f)) != EOF) {
    //     printf("%02X", c);
    // }
    // puts("\ndone");
    // execl(&path[1], &path[1], (char *)NULL);
    // errExit("execl");
    // ERROR [ENOENT No such file or directory] execl
    // puts("Going to spawn");
    // _spawnlp(P_OVERLAY, &path[1], &path[1], NULL);
    // spawn failed: No such file or directory
    // perror("spawn failed");
    // puts("Still running?");
    // execl("/bin/sh", "sh", "-c", "date", (char *)NULL);
    // errExit("execl");
    // const char path[] = "./readflag";
    // const char path[] = "/readflag";
    // const char path[] = "\\readflag";
    const char path[] = "\\\\readflag";
    execl(path, path, (char *)NULL);
    errExit("execl");
    // return 0;
}
