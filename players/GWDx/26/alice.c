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

    char secret[100];
    // open file /secret and read
    FILE* fp = fopen("/secret", "r");
    if (fp == NULL) {
        printf("open file failed");
        exit(1);
    }
    fgets(secret, 100, fp);

    //创建key值
    if (key == -1) {
        perror("ftok");
    }

    //创建共享内存
    shmid = shmget(key, BUFSZ, IPC_CREAT | 0666);
    if (shmid < 0) {
        perror("shmget");
        exit(-1);
    }

    //映射
    shmadd = shmat(shmid, NULL, 0);
    if (shmadd < 0) {
        perror("shmat");
        _exit(-1);
    }

    // print shared memory id
    printf("shared memory id: %d\n", shmid);

    //拷贝数据至共享内存区
    printf("copy data to shared-memory\n");
    bzero(shmadd, BUFSZ);  // 共享内存清空
    strcpy(shmadd, secret);

    return 0;
}
