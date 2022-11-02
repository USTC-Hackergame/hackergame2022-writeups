#include <fcntl.h>
#include <unistd.h>

#include "common.h"

int main() {
    int msqid = msgget(SERVER_KEY, IPC_CREAT | S_IRUSR | S_IWUSR);
    if (msqid == -1) {
        errExit("msgget");
    }

    msg_t msg;
    if (msgrcv(msqid, &msg, sizeof(msg.content), 1, 0) == -1) {
        errExit("msgrcv");
    }

    ssize_t num_written = write(STDOUT_FILENO, msg.content, sizeof(msg.content));
    if (num_written != sizeof(msg.content)) {
        errExit("wrote %ld bytes", (long)num_written);
    }

    return 0;
}
