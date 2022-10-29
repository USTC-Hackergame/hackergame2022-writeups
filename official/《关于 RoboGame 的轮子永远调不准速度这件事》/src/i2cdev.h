#pragma once
#include <cstdint>
#include <vector>
#include <array>
#include "emu8051/emu8051.h"
using namespace std;
typedef emu8051 e8;
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;

#define I2C_STAT            0xe1
#define I2C_XRAM_LOW        0xe2
#define I2C_XRAM_HIGH       0xe3
#define I2C_BUF_SIZE        0xe4
#define I2C_ADDR            0xe6
#define I2C_RW              0xe7
#define I2C_STAT_READY      0
#define I2C_STAT_BUSY       1
#define I2C_STAT_NOTFOUND   2
#define I2C_STAT_DEV_ERR    3


class I2CDev{
    public:
        typedef bool (*I2C_dev_hndl)(e8*,e8::access_type_t,u8,void*,u16 sz,void *data);
        I2CDev(e8 *emu);
        void reg_dev_hndl(u8,I2C_dev_hndl,void*);

    private:
        static bool sfr_fder(e8*,e8::access_type_t,e8::address_type_t,u8,u8*,void*);
        bool sfr_hndl(e8::access_type_t,e8::address_type_t,u8,u8*);
        void sfr_hndl_exec(u8);
        void i2c_hndl_w();
        void i2c_hndl_r();
        e8 *emuaddr;
        array<I2C_dev_hndl,0x80> i2c_hndl_arr{};
        array<void*,0x80> i2c_hndl_data_arr{};
        u8 reg_stat=0;
        u8 reg_xram_low=0;
        u8 reg_xram_high=0;
        u8 reg_buf_sz=0;
        u8 reg_i2c_addr=0;
};

I2CDev::I2CDev(e8* emu){
    emuaddr=emu;
    for(u32 reg:{
        I2C_STAT,
        I2C_XRAM_LOW,
        I2C_XRAM_HIGH,
        I2C_BUF_SIZE,
        I2C_ADDR,
        I2C_RW
    }){
        emuaddr->sfr_register_handler(reg,I2CDev::sfr_fder,this);
    }
}
void I2CDev::reg_dev_hndl(u8 addr,I2C_dev_hndl hndl,void* data){
    i2c_hndl_arr.at(addr)=hndl;
    i2c_hndl_data_arr.at(addr)=data;
}

bool I2CDev::sfr_fder(e8* emu,e8::access_type_t access_type,e8::address_type_t addr_type,u8 addr,u8* val,void* data){
    return ((I2CDev*)data)->sfr_hndl(access_type,addr_type,addr,val);
}

bool I2CDev::sfr_hndl(e8::access_type_t access_type,e8::address_type_t addr_type,u8 addr,u8*val){
    if(access_type==e8::access_type_t::READ){
        switch (addr){
            case I2C_STAT:
            *val=reg_stat;
            return 1;

            case I2C_XRAM_LOW:
            *val=reg_xram_low;
            return 1;

            case I2C_XRAM_HIGH:
            *val=reg_xram_high;
            return 1;

            case I2C_BUF_SIZE:
            *val=reg_buf_sz;
            return 1;
            
            case I2C_ADDR:
            *val=reg_i2c_addr;

            case I2C_RW:
            *val=0;
            return 1;

            default:
            fprintf(stderr,"E2:I2C line %d\n",__LINE__);
            exit(1);
        }
    }
    else{
        switch(addr){
            case I2C_STAT:
            return 1;

            case I2C_XRAM_LOW:
            reg_xram_low=*val;
            return 1;

            case I2C_XRAM_HIGH:
            reg_xram_high=*val;
            return 1;

            case I2C_BUF_SIZE:
            reg_buf_sz=*val;

            case I2C_ADDR:
            reg_i2c_addr=*val&0x7f;
            return 1;

            case I2C_RW:
            this->sfr_hndl_exec(*val);
            return 1;
            
            default:
            fprintf(stderr,"E2:I2C line %d\n",__LINE__);
            exit(1);
        }
    }
    return 1;
}

void I2CDev::sfr_hndl_exec(u8 inst){
    if(!(i2c_hndl_arr.at(reg_i2c_addr))){
        reg_stat=I2C_STAT_NOTFOUND;
        return;
    }
    switch(inst&1){
        case 0:
        this->i2c_hndl_w();
        return;
        case 1:
        this->i2c_hndl_r();
        return;
    }
}

void I2CDev::i2c_hndl_w(){
    vector<u8> buf;
    buf.resize(reg_buf_sz);
    if(reg_buf_sz){
        u16 xram_addr=(((u16)reg_xram_high)<<8)|reg_xram_low;
        array<u8,0x10000>&xram=emuaddr->xram_get_direct();
        for(u32 i=0;i<reg_buf_sz;i++){
            buf.at(i)=xram.at(xram_addr);
            xram_addr++;
        }
    }
    auto hndl=i2c_hndl_arr.at(reg_i2c_addr);
    if(hndl(emuaddr,e8::access_type_t::WRITE,reg_i2c_addr,&buf[0],buf.size(),i2c_hndl_data_arr.at(reg_i2c_addr))) reg_stat=I2C_STAT_READY;
    else reg_stat=I2C_STAT_DEV_ERR;
}

void I2CDev::i2c_hndl_r(){
    vector<u8> buf;
    buf.resize(reg_buf_sz);
    auto hndl=i2c_hndl_arr.at(reg_i2c_addr);
    if(hndl(emuaddr,e8::access_type_t::READ,reg_i2c_addr,&buf[0],buf.size(),i2c_hndl_data_arr.at(reg_i2c_addr))) reg_stat=I2C_STAT_READY;
    else reg_stat=I2C_STAT_DEV_ERR;
    if(!reg_buf_sz) return;
    u16 xram_addr=(((u16)reg_xram_high)<<8)|reg_xram_low;
    array<u8,0x10000>&xram=emuaddr->xram_get_direct();
    for(u32 i=0;i<reg_buf_sz;i++){
        xram.at(xram_addr)=buf.at(i);
        xram_addr++;
    }
}