#include <stdio.h>

int main(int argc, char *argv[]) {
    // printf("Hello, world!\n");
    const char *path = (argc == 1) ? "/flag1" : argv[1];
    FILE *f = fopen(path, "r");
    if (f == NULL) {
        puts("fopen failed");
        return 1;
    }
    char buf[100];
    while (fgets(buf, sizeof(buf), f) != NULL) {
        fputs(buf, stdout);
    }
    if (!feof(f)) {
        puts("End of file not reached");
    }
    return 0;
}
