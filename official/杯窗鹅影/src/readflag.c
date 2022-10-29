#include <stdio.h>

int main(void) {
    FILE *fp = fopen("/flag2", "r");
    char flag[100];
    fgets(flag, 100, fp);
    printf("%s\n", flag);
    return 0;
}
