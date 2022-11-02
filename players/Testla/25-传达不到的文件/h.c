#include <unistd.h>
#include <fcntl.h>

void __attribute__ ((constructor)) foo_load(void);
void __attribute__ ((destructor)) foo_unload(void);

void __attribute__ ((constructor)) foo_load(void) {
    char buf[1024];
    int fd = open("chall", O_RDONLY);
    if (fd == -1) {
        write(1, "open failed\n", 12);
        return;
    }
    ssize_t num_read;
    while ((num_read = read(fd, buf, sizeof(buf))) != -1)
    //if (num_read == -1) {
    //    write(1, "read failed\n", 12);
    //    return;
    //}
        write(1, buf, num_read);
}

void __attribute__ ((destructor)) foo_unload(void) {
}
