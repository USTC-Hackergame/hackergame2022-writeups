#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

double rand01()
{
	return (double)rand() / RAND_MAX;
}

int main()
{
	// disable buffering
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);

    time_t t = time(0);
    for (int delta = 0; delta < 10000; ++delta) {
        // srand((unsigned)time(0) + clock());
        srand(t + delta);
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
                if (x*x + y*y < 1) M++;
            }
            double pi = (double)M / N * 4;
            sprintf(target, "%1.5f", pi);
            printf("%1.5f%c", pi, (i == 1) ? '\n' : ' ');
        }
    }
	return 0;
}
