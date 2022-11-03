#include <stdio.h>
#include <fcntl.h>
#include <mqueue.h>
#include <unistd.h>


int main(void)
{
    sleep(1);  // wait for Alice
    mqd_t mq = mq_open("/msgqueue", O_RDONLY);
    if (mq < 0) {
        perror("mq_open");
        return 1;
    }

    char buf[1024];
    if (mq_receive(mq, buf, 1024, 0) < 0) {
        perror("mq_receive");
        return 1;
    }

    printf("%s", buf);

    if (mq_unlink("/msgqueue") < 0) {
        perror("mq_unlink");
        return 1;
    }
    return 0;
}
