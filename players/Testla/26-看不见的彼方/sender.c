#include <fcntl.h>
#include <unistd.h>

#include "common.h"

int main() {
    int fd = open("/secret", O_RDONLY);
    if (fd == -1) {
        errExit("open");
    }

    msg_t msg;
    msg.mtype = 1;
    ssize_t num_read = read(fd, msg.content, sizeof(msg.content));
    if (num_read != sizeof(msg.content)) {
        errExit("read %d bytes", num_read);
    }

    int msqid = msgget(SERVER_KEY, IPC_CREAT | S_IRUSR | S_IWUSR);
    if (msqid == -1) {
        errExit("msgget");
    }

    if (msgsnd(msqid, &msg, sizeof(msg.content), 0) == -1) {
        errExit("msgsnd");
    }

    return 0;
}
