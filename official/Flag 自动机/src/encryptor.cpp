#include "encryptor.h"
#include "defs.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ROTATE_LEFT(x, n) ((x) << (n)) | ((x) >> ((10) - (n)))
#define ROTATE_RIGHT(x, n) ((x) >> (n)) | ((x) << ((10) - (n)))

unsigned char key[] = "Kanbe_Kotori";
unsigned char box[43];
unsigned char encrypted[43] = {0x19, 0x1b, 0xe8, 0xed, 0x82, 0xcf, 0x33, 0xb1, 0xd9, 0x10, 0x10, 0xf7, 0xf3, 0x2b, 0x3e, 0x20, 0x2, 0xdd, 0x2e, 0xb9, 0x8f, 0x39, 0x15, 0xb6, 0xf8, 0x58, 0xc, 0xce, 0x68, 0xe, 0x93, 0xdf, 0x2e, 0xca, 0x43, 0x8f, 0x9c, 0xe8, 0xaa, 0x7e, 0xd2, 0x43, 0xc1};
unsigned char output[43];

unsigned char getnum(int num){
    if (num == 0)   return 0x19;
    if (num == 1)   return 0x11;
    if (num == 2)   return 0x45;
    if (num == 3)   return 0x14;
    return 0;
}

void initBox(void){
    for (int i = 0; i < 13; i++){
        for (int j = 0; j < 4; j++){
            box[(i * 4 + j) % 43] = (__ROL1__(key[(i * 13 + j) % 13], getnum((j * 11) % 4) % 8) % 256);
            box[(i * 4 + j) % 43] ^= (key[(i * 4 + j) % 13] + getnum((j) % 4)) % 256;
            box[(i * 4 + j) % 43] ^= (__ROR1__(key[(i * 13 + j) % 13], getnum((i * 11) % 4) % 8) % 256);
        }
    }

    for (int i = 0; i < 43; i++)    printf("%d ", box[i]);
    printf("\n");
}

void decrypt(){
    for (int i = 0; i < 43; i++){
        encrypted[i] = (encrypted[i] - (box[i] + key[i * 11 % 13]) * getnum((i * 13) % 4)) ^ box[i];
    }
}

unsigned char *getflag(HWND hwnd, LPARAM LParam)
{
    initBox();
    decrypt();

    printf("%s", encrypted);

    unsigned char *ret = (unsigned char *)malloc(sizeof(encrypted));
    strncpy((char *)ret, (char *)encrypted, sizeof(encrypted));

	return ret;
}