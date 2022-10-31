#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

double rand01() {
    return (double)rand() / RAND_MAX;
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    int time0 = time(0);

    char buf1[100] = "3.13801";
    char buf2[100] = "3.14753";

    for (int clock0 = 0; clock0 < 2000; clock0++) {
        srand((unsigned)time0 + clock0);

        int games = 5;
        int win = 0;
        int lose = 0;
        char target[20];
        char guess[2000];
        for (int i = games; i > 0; i--) {
            int M = 0;
            int N = 400000;
            for (int j = 0; j < N; j++) {
                double x = rand01();
                double y = rand01();
                if (x * x + y * y < 1)
                    M++;
            }
            double pi = (double)M / N * 4;
            sprintf(target, "%1.5f", pi);

            if (i == 5) {
                if (strcmp(target, buf1) != 0)
                    break;
            } else if (i == 4) {
                if (strcmp(target, buf2) != 0)
                    break;
            } else
                printf("clock0 = %d, i = %d, target = %s\n", clock0, i, target);
        }
    }
    return 0;
}
