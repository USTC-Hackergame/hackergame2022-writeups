#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <poll.h>
#include <initializer_list>
#include "emu8051/emu8051.h"
#pragma once
typedef emu8051 e8;
typedef uint8_t u8;
typedef uint32_t u32;
#define SERIAL_OUT_DATA 0xf2
#define SERIAL_OUT_READY 0xf3
#define SERIAL_IN_DATA 0xfa
#define SERIAL_IN_READY 0xfb

class serialDev{
    public:

        serialDev(e8*);

    private:
        static bool sfr_fder(e8 *,e8::access_type_t,e8::address_type_t,u8,u8*,void*);
        bool sfr_hndl(e8::access_type_t,e8::address_type_t,u8,u8*);
        bool sfr_hndl_read_data(u8 *);
        bool sfr_hndl_read_ready(u8 *);
        bool sfr_hndl_write_data(u8);
        void upd_stdin_stat();
        e8 *emu_addr;
        u8 input_byte;
        bool input_ready=0;
};

serialDev::serialDev(e8 *emu){
    emu_addr=emu;
    for(u32 reg:{
        SERIAL_OUT_DATA,
        SERIAL_OUT_READY,
        SERIAL_IN_DATA,
        SERIAL_IN_READY}){
            emu_addr->sfr_register_handler(reg,serialDev::sfr_fder,this);
        }
}

bool serialDev::sfr_fder(
    e8 *emu,
    e8::access_type_t access_type,
    e8::address_type_t addr_type,
    u8 addr,
    u8 *val,
    void* data){
    return ((serialDev*)data)->sfr_hndl(access_type,addr_type,addr,val);
}

bool serialDev::sfr_hndl(
    e8::access_type_t access_type,
    e8::address_type_t addr_type,
    u8 addr,
    u8 *val
){
    if(access_type==e8::access_type_t::READ){
        switch(addr){
            case SERIAL_OUT_DATA:
            *val=0;
            return 1;

            case SERIAL_OUT_READY:
            *val=1;
            return 1;

            case SERIAL_IN_DATA:
            return this->sfr_hndl_read_data(val);

            case SERIAL_IN_READY:
            return this->sfr_hndl_read_ready(val);

            default:
            fprintf(stderr,"E1: Serial line %d\n",__LINE__);
            exit(1);
        }
    }
    else{
        switch(addr){
            case SERIAL_OUT_DATA:
            return this->sfr_hndl_write_data(*val);
            case SERIAL_IN_DATA:
            case SERIAL_OUT_READY:
            case SERIAL_IN_READY:
            return 1;
            default:
            fprintf(stderr,"E1: Serial line %d\n",__LINE__);
            exit(1);
        }
    }
}

bool serialDev::sfr_hndl_read_data(u8 *val){
    this->upd_stdin_stat();
    if(!input_ready){
        *val=0;
        return 1;
    }
    *val=input_byte;
    input_ready=0;
    return 0;
}

bool serialDev::sfr_hndl_read_ready(u8 *val){
    this->upd_stdin_stat();
    *val=(u8)input_ready;
    return 1;
}

bool serialDev::sfr_hndl_write_data(u8 val){
    putchar((int)val);
    return 1;
}

void serialDev::upd_stdin_stat(){
    if(input_ready) return;
    pollfd stdin_fd={0,POLLIN,0};
    int ret=poll(&stdin_fd,1,0);
    if(ret<=0||!(stdin_fd.revents&POLLIN)) return;
    int ch=getchar();
    if(ch==EOF) return;
    input_byte=ch;
    input_ready=1;
}

