#include <stdint.h>
#include <stdbool.h>
typedef uint8_t u8;
int main(){
    return 0;
}
void func(){
    __asm
    mov r0,#0
$0001:
    mov dptr,#0xe00
    mov a,r0
    movc a,@a+dptr
    mov r1,a

    mov dptr,#0xe80
    mov a,r0
    movc a,@a+dptr
    orl a,r1
    mov r4,a
$0002:
    mov a,0xf3
    jz $0002

    inc r0
    mov a,r4
    mov 0xf2,a

    jnz $0001
    __endasm;
}