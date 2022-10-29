#include <stdio.h>

#define rd(t) f = fopen("./data/static." #t, "rb"); fread(t, 1, 1024, f); fclose(f);

#define N 5
char in[1024];
char out[1024];
char s[1024];

int main() {
    scanf("%s", s);
    FILE *f = NULL;
    rd(in);
    rd(out);
    printf("%s", out);

}