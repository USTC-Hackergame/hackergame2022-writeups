#include <sys/sysinfo.h>
#include <stdio.h>
#include <unistd.h>

int main() {
    struct sysinfo info;
    unsigned short prev_procs;
    int bit_count = 0;
    int hex = 0;

    sleep(1);

    sysinfo(&info);
    prev_procs = info.procs;

    while (bit_count < 256) {
        sysinfo(&info);

        if (info.procs < prev_procs) {
            bit_count += 1;
            hex <<= 1;
        } else if (info.procs > prev_procs) {
            bit_count += 1;
            hex = (hex << 1) + 1;
        } else {
            continue;
        }

        if (bit_count % 4 == 0) {
            printf("%x", hex);
            hex = 0;
        }

        prev_procs = info.procs;
    }

    putchar('\n');

    return 0;
}
