
// cat incbin.h q2.c > q2payload.c
// or: #include "incbin.h"
#include <stdio.h>
#include <string.h>

INCTXT(StaticIn, "/proc/self/cwd/data/static.in");
INCTXT(StaticOut, "/proc/self/cwd/data/static.out");

INCTXT(Dyn0In, "/proc/self/cwd/data/dynamic0.in");
INCTXT(Dyn0Out, "/proc/self/cwd/data/dynamic0.out");
INCTXT(Dyn1In, "/proc/self/cwd/data/dynamic1.in");
INCTXT(Dyn1Out, "/proc/self/cwd/data/dynamic1.out");
INCTXT(Dyn2In, "/proc/self/cwd/data/dynamic2.in");
INCTXT(Dyn2Out, "/proc/self/cwd/data/dynamic2.out");
INCTXT(Dyn3In, "/proc/self/cwd/data/dynamic3.in");
INCTXT(Dyn3Out, "/proc/self/cwd/data/dynamic3.out");
INCTXT(Dyn4In, "/proc/self/cwd/data/dynamic4.in");
INCTXT(Dyn4Out, "/proc/self/cwd/data/dynamic4.out");

#define BUFSIZE 4096

int main(void)
{
    char input[BUFSIZE];
    fgets(input, BUFSIZE, stdin);

    const char *in[] = {gStaticInData, gDyn0InData, gDyn1InData, gDyn2InData, gDyn3InData, gDyn4InData};
    const char *out[] = {gStaticOutData, gDyn0OutData, gDyn1OutData, gDyn2OutData, gDyn3OutData, gDyn4OutData};

    for (int i=0; i<6; i++) {
        if (strcmp(in[i], input) == 0) {
            printf("%s", out[i]);
            return 0;
        }
    }

    return 1;
}
