#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>
#include <signal.h>

pid_t pid_list[512];
int n_proc;

void send0() {
    pid_t pid = pid_list[--n_proc];
    int status;
    //printf("0");
    kill(pid, SIGTERM);
    waitpid(pid, &status, 0);
}

void send1() {
    pid_t pid;
    //printf("1");
    if ((pid = fork()) == 0) {
        sleep(10);
        exit(0);
    } else {
        pid_list[n_proc++] = pid;
    }
}

int main() {
    FILE *fin = fopen("secret", "r");

    for (int i=0; i<256; i++)
        send1();

    sleep(2);

    for (int i=0; i<64; i++) {
        char c = fgetc(fin);
        c = c >= 'a' ? c - 'a' + 10 : c - '0';

        for (int j=3; j>=0; j--) {
            usleep(10000);
            if ((c >> j) & 1) send1(); else send0();
        }
    }

    fclose(fin);

    return 0;
}
