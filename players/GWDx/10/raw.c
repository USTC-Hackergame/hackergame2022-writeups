#include <stdio.h>

#include "incbin.h"

INCTXT(staticOut, "./data/static.out");
INCTXT(dynamic0Out, "./data/dynamic0.out");
INCTXT(dynamic1Out, "./data/dynamic1.out");
INCTXT(dynamic2Out, "./data/dynamic2.out");
INCTXT(dynamic3Out, "./data/dynamic3.out");
INCTXT(dynamic4Out, "./data/dynamic4.out");

int main(int argc, char* argv[]) {
    // read currentFile from currentFile,
    // if not exist, create it, currentFile = 0
    FILE* fp = fopen("./temp/currentFile", "r");
    int currentFile = 0;
    if (fp != NULL) {
        fscanf(fp, "%d", &currentFile);
        fclose(fp);
    }
    // write currentFile + 1 to currentFile
    fp = fopen("./temp/currentFile", "w");
    fprintf(fp, "%d", currentFile + 1);
    fclose(fp);

    // if currentFile = 0, print gstaticOutData
    // if currentFile = 1, print gdynamic0OutData
    if (currentFile == 0)
        printf("%s", gstaticOutData);
    else if (currentFile == 1)
        printf("%s", gdynamic0OutData);
    else if (currentFile == 2)
        printf("%s", gdynamic1OutData);
    else if (currentFile == 3)
        printf("%s", gdynamic2OutData);
    else if (currentFile == 4)
        printf("%s", gdynamic3OutData);
    else if (currentFile == 5)
        printf("%s", gdynamic4OutData);
}
