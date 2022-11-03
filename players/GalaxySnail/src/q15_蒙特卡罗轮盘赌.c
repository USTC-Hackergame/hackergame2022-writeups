#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>


static inline double rand01(void)
{
    return (double)rand() / RAND_MAX;
}


double calc_pi(char pi_str[static 10])
{
    int M = 0;
    int N = 400000;
    for (int j = 0; j < N; j++) {
        double x = rand01();
        double y = rand01();
        if (x*x + y*y < 1) M++;
    }
    double pi = (double)M / N * 4;
    sprintf(pi_str, "%1.5f", pi);
    return pi;
}


void usage(const char *prog, FILE *f)
{
    fprintf(f, "%s <expect1> <expect2>\n", prog);
}


int main(int argc, char *argv[])
{

    if (argc < 3) {
        usage(argv[0], stderr);
        return 1;
    }
    if (!strcmp(argv[1], "-h") || !strcmp(argv[1], "--help")) {
        usage(argv[0], stdout);
        return 0;
    }

    const char *expect1 = argv[1];
    const char *expect2 = argv[2];

    unsigned int seed_start, seed_end;
    seed_start = time(NULL);
    seed_end = seed_start + 2048;

    char pi_str[10];
    unsigned int seed;
    for (seed = seed_start; seed <= seed_end; seed++) {
        srand(seed);
        calc_pi(pi_str);
        if (strcmp(pi_str, expect1) != 0) continue;
        calc_pi(pi_str);
        if (strcmp(pi_str, expect2) != 0) continue;

        printf("Woo hoo! The seed is %u\n", seed);
        goto succeed;
    }

    printf("Unfortunately, not found.\n");
    return 1;

succeed:
    for (int i=0; i < 3; i++) {
        calc_pi(pi_str);
        printf("%s\n", pi_str);
    }
    return 0;
}
