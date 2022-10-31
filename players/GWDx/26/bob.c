#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>

#define BUFSZ 512

int main(int argc, char* argv[]) {
    int shmid;
    int ret;
    key_t key = 0x1234;
    char* shmadd;

    //打开共享内存
    shmid = shmget(key, BUFSZ, IPC_CREAT | 0666);

    //映射
    shmadd = shmat(shmid, NULL, 0);

    //读共享内存区数据
    printf("%s", shmadd);

    //分离共享内存和当前进程
    ret = shmdt(shmadd);

    //删除共享内存
    shmctl(shmid, IPC_RMID, NULL);

    system("ipcs -m");  //查看共享内存

    return 0;
}
