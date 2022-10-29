#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <unistd.h>
#include <signal.h>
#include "emu8051/emu8051.h"
#include "serial.h"
#include "i2cdev.h"
#include "wheel.h"
#include "eeprom.h"

typedef emu8051 e8;
typedef uint8_t u8;
volatile bool tag_exit;
volatile bool tag_alarm;
void sig_hndl(int);
bool sfr_off(e8 *,e8::access_type_t,e8::address_type_t,uint8_t,uint8_t*,void*);
bool sfr_save(e8 *,e8::access_type_t,e8::address_type_t,uint8_t,uint8_t*,void*);
void bufinit();
void banner();

int main(){
    
    bufinit();
    banner();
    e8 emu;
    serialDev serial(&emu);
    I2CDev i2cdev(&emu);
    wheelDev wheeldev(&emu,&i2cdev);
    eepromDev eepromdev(&emu,&i2cdev,0x24);

    const size_t eeprom_sz=4096;
    eepromdev.set_cap(eeprom_sz);

    FILE *fp=fopen("firmware","rb");
    u8 pmem_img[0x10000],flag1[128],flag2[128],hidden[64];
    memset(pmem_img, 0xff, sizeof(pmem_img));
    fread(pmem_img, 1, sizeof(pmem_img), fp);
    fclose(fp);
    eepromdev.store(0,pmem_img,eeprom_sz);

    emu.sfr_register_handler(0xff, sfr_off, 0);
    emu.sfr_register_handler(0xfe, sfr_save, 0);
    signal(SIGALRM, sig_hndl);
    alarm(120);

    int inst_cnt = 0;
    while(1) {
        if(inst_cnt == 1000){
            usleep(6 * 1000);
            inst_cnt = 0;
        }
        else inst_cnt++;
        emu.execute(1);
        if(tag_exit) break;
    }
    if (tag_alarm) puts("timeout");
    else puts("poweroff");
    return 0;
}
void banner(){
    FILE* fp=fopen("banner","rb");
    char s[3000];
    fread(s,1,3000,fp);
    puts(s);
    fclose(fp);
}
void sig_hndl(int signum){
    tag_exit=1;
    tag_alarm=1;
}
bool sfr_off(
    e8 *emu,
    e8::access_type_t access_type,
    e8::address_type_t addr_type,
    uint8_t addr,
    uint8_t *val,
    void* data){
    if(access_type==e8::access_type_t::READ){
        *val=0;
        return 1;
    }
    tag_exit=1;
    return 1;
}
bool sfr_save(
    e8 *emu,
    e8::access_type_t access_type,
    e8::address_type_t addr_type,
    uint8_t addr,
    uint8_t *val,
    void* data){
    usleep(100000);
    return 1;
}
void bufinit(){
    setvbuf(stdin,0,2,0);
    setvbuf(stdout,0,2,0);
    setvbuf(stderr,0,2,0);
}
