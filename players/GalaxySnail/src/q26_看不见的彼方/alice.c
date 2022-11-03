#include <stdio.h>
#include <fcntl.h>
#include <mqueue.h>
#include <unistd.h>


int main(void)
{
    if (mq_unlink("/msgqueue") < 0) {
        perror("mq_unlink");
    }

    mqd_t mq;
    struct mq_attr attr = {
        .mq_maxmsg = 10,
        .mq_msgsize = 1024,
    };
    mq = mq_open("/msgqueue", O_RDWR | O_CREAT, 0600, &attr);
    if (mq < 0) {
        perror("mq_open");
        return 1;
    }

    int fd = open("/secret", O_RDONLY);
    if (fd < 0) {
        perror("open");
        return 1;
    }

    char buf[1024];
    ssize_t ret;
    if ((ret = read(fd, buf, 64)) < 0) {
        perror("read");
        return 1;
    }
    buf[ret] = '\0';
    printf("msg: |%s|\n", buf);

    if (mq_send(mq, buf, 1024, 0) < 0) {
        perror("mq_send");
        return 1;
    }

    return 0;
}

