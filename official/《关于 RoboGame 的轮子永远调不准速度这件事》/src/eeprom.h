#pragma once
#include <cstdint>
#include <vector>
#include "emu8051/emu8051.h"
#include "i2cdev.h"
using namespace std;
typedef emu8051 e8;
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
int leftbits=9;
u16 minof(u16 a,u16 b){
    if(a<b) return a;
    return b;
}
class eepromDev{
    public:
        eepromDev(e8*,I2CDev *,uint8_t );
        void set_cap(u32);
        void store(u16,u8 *,u16);

    private:
        static void pmem_fder(e8*,e8::access_type_t,u16,u8*,void*);
        void pmem_ctrl(e8::access_type_t,u16,u8*);
        static bool i2c_fder(e8*,e8::access_type_t,u8,void*,u16,void*);
        bool i2c_hndl(e8::access_type_t,u8,void*,u16);
        e8* emuaddr;
        u8 i2c_addr{};
        u8 reg_i2c_page{};
        vector<u8> mem;
};

eepromDev::eepromDev(e8* emu,I2CDev *i2cdev,u8 addr){
    emuaddr=emu;
    emuaddr->pmem_register_controller(eepromDev::pmem_fder,this);
    i2c_addr=addr;
    i2cdev->reg_dev_hndl(addr,eepromDev::i2c_fder,this);
}

void eepromDev::set_cap(u32 new_cap){
    if(new_cap==512||new_cap==1024||new_cap==2048||new_cap==4096){
        mem.resize(new_cap);
        return;
    } 
    fprintf(stderr, "E3:eeprommem resize\n");
    exit(1);
}

void eepromDev::store(u16 bs,u8 *data,u16 sz){
    for(u32 i=0;i<sz;i++) mem.at(i+bs)=data[i];
}

void eepromDev::pmem_fder(e8 *emu,e8::access_type_t access_type,u16 addr,u8 *val,void *data){
    ((eepromDev*)data)->pmem_ctrl(access_type,addr,val);
}

void eepromDev::pmem_ctrl(e8::access_type_t access_type,u16 addr,u8 *val){
    if(access_type==e8::access_type_t::WRITE) return;
    if(!mem.size()){
        fprintf(stderr,"E4:eeprommem cap zero\n");
        exit(1);
    }
    const u16 masked_addr=addr&(mem.size()-1);
    *val=mem.at(masked_addr);
}

bool eepromDev::i2c_fder(e8 *emu,e8::access_type_t access_type,u8 addr,void *buf,u16 sz,void *data){
    return ((eepromDev*)data)->i2c_hndl(access_type,addr,buf,sz);
}

int diffBitsCount(u8 a,u8 b){
    u8 x=a^b;
    int cnt=0;
    while(x){
        if(x&1) cnt++;
        x>>=1;
    }
    return cnt;
}

bool eepromDev::i2c_hndl(e8::access_type_t access_type,u8 addr,void* buf,u16 sz){
    u8* buf_arr=(u8*)buf;
    const u8 page_max=(u8)(mem.size()>>6);
    if(access_type==e8::access_type_t::WRITE){
        if(sz>=1) reg_i2c_page=buf_arr[0]&(page_max-1);
        int clr_mask_cnt=minof(sz-1,64);
        u8 *clr_mask=buf_arr+1;
        for(u32 i=0;i<clr_mask_cnt;i++){
            //printf(">>> %02x , %x ->",mem.at(reg_i2c_page*64+i),clr_mask[i]);
            u8 a=mem.at(reg_i2c_page*64+i),b=clr_mask[i];
            int diffcnt;
            b=a&~b;
            diffcnt=diffBitsCount(a,b);
            if(diffcnt<=leftbits){
                mem.at(reg_i2c_page*64+i)=b;
                leftbits-=diffcnt;
            }
            else{
                puts("No bits left!");
            }
            //printf(">>> %x\n",mem.at(reg_i2c_page*64+i));
        }
        return 1;
    }
    else if(access_type==e8::access_type_t::READ){
        int req_cnt=minof(sz,64);
        for(u32 i=0;i<req_cnt;i++){
            buf_arr[i]=mem.at(reg_i2c_page*64+i);
        }
        return 1;
    }
}