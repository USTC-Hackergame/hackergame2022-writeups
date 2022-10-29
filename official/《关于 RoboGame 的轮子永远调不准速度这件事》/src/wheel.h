#pragma once
#include <initializer_list>
#include <unistd.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include "emu8051/emu8051.h"
#include "i2cdev.h"
#define WHL_PORT_BASE 100
typedef emu8051 e8;
typedef uint8_t u8;
typedef uint16_t u16;
u8 flag[0x24],solve=0,lefttimes=27;
class wheelDev{
    public:
    wheelDev(e8 *,I2CDev *i2cdev);

    private:
    static bool i2c_fder(e8*,e8::access_type_t,u8,void*,u16,void*);
    bool i2c_hndl(e8::access_type_t,u8,void*,u16);
    e8 *emuaddr;
    u8 speed[0x24]={
        0x11,0x45,0x14,0x19,0x19,0x81,0x00,0x00,
        0x11,0x45,0x14,0x19,0x19,0x81,0x00,0x00,
        0x11,0x45,0x14,0x19,0x19,0x81,0x00,0x00,
        0x11,0x45,0x14,0x19,0x19,0x81,0x00,0x00,
        0x11,0x45,0x14,0x19,
    };
};
wheelDev::wheelDev(e8* emu,I2CDev* i2cdev){
    emuaddr=emu;
    for(u8 i=0;i<0x24;i++){
        i2cdev->reg_dev_hndl(i,wheelDev::i2c_fder,this);
    }
    FILE* fd=fopen("flag","rb");
    fread(flag,1,0x24,fd);
}
bool wheelDev::i2c_fder(e8* emu,e8::access_type_t access_type,u8 addr,void* buf,u16 sz,void* data){
    return ((wheelDev*)data)->i2c_hndl(access_type,addr,buf,sz);
}

int check(u8 arr[]){
    for(int i=0;i<8;i++)
        if(arr[i]!=arr[i+1]) return 0;
    return 1;
}
bool wheelDev::i2c_hndl(e8::access_type_t access_type,u8 addr,void *buf,u16 sz){
    if(access_type==e8::access_type_t::WRITE && !solve ){
        if(lefttimes){
            speed[addr]=*(u8*)buf;
            lefttimes-=1;
            if(check(speed)){
                puts("Congrats! Flag is in the speed data of all wheels.");
                memcpy(speed,flag,0x24);
                solve=1;
            }
        }
        else{
            puts("No more chance to set speed!");
        }
    }
    else if(access_type==e8::access_type_t::READ){
        //sprintf((char*)buf,"%2.6f%%",(float)speed[addr-WHL_PORT_BASE]);
        *(u8*)buf=speed[addr];
    }
    return 1;
}