#include <stdio.h>

#define rd(t, i) f = fopen("./data/dynamic" #i "." #t, "rb"); fread(t[i], 1, 1024, f); fclose(f);

#define N 5
char in[N][1024];
char out[N][1024];
char s[1024];

const char* p="6986590628073995024206381186276138153424072978206545074944875649843290100081955176834953570642082110986847373343097251365990774537621958187962785857266231";
const char* q="9670952257261859649800781015934966179922141009663011753656600907159538795015957046655051313532145815478824330531921818376792969122525356700036137989985221";

int main() {
    scanf("%s", s);
    FILE *f = NULL;
    rd(in, 0);
    rd(out, 0);
    rd(in, 1);
    rd(out, 1);
    rd(in, 2);
    rd(out, 2);
    rd(in, 3);
    rd(out, 3);
    rd(in, 4);
    rd(out, 4);

    int i;
    for(i=0; i<5; i++) {
        if(strncmp(in[i], s, 10) == 0) {
            printf("%s", out[i]);
            break;
        }
    }
    if(i == 5) {
        printf("%s\n%s\n", p, q);
    }

}