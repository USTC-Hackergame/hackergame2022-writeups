#include <unistd.h>
#include <sys/types.h>

#include<sys/ptrace.h>
#include<sys/reg.h>
#include<sys/wait.h>
#include<sys/user.h>
#include<stdlib.h>
#include<errno.h>
#include<string.h>
#include<stdio.h>

#include <sys/stat.h>
#include <fcntl.h>

#include <stdint.h>
#include <sys/syscall.h>

#define long_size sizeof(long)

void print_regs(struct user_regs_struct regs)
{
    printf("+++++++ return from syscall ++++++++\n");
    printf("RAX:    %#lx\n", regs.rax);
    printf("RBX:    %#lx\n", regs.rbx);
    printf("RCX:    %#lx\n", regs.rcx);
    printf("RDX:    %#lx\n", regs.rdx);
    printf("RSI:    %#lx\n", regs.rsi);
    printf("RDI:    %#lx\n", regs.rdi);
    printf("RBP:    %#lx\n", regs.rbp);
    printf("RSP:    %#lx\n", regs.rsp);
    printf("RIP:    %#lx\n", regs.rip);
    printf("R8:     %#lx\n", regs.r8);
    printf("R9:     %#lx\n", regs.r9);
    printf("R10:    %#lx\n", regs.r10);
    printf("R11:    %#lx\n", regs.r11);
    printf("R12:    %#lx\n", regs.r12);
    printf("R13:    %#lx\n", regs.r13);
    printf("R14:    %#lx\n", regs.r14);
    printf("R15:    %#lx\n", regs.r15);
    printf("EFLAGS: %#lx\n", regs.eflags);
    printf("CS:     %#lx\n", regs.cs);
    printf("SS:     %#lx\n", regs.ss);
    printf("DS:     %#lx\n", regs.ds);
    printf("ES:     %#lx\n", regs.es);
    printf("FS:     %#lx\n", regs.fs);
    printf("GS:     %#lx\n", regs.gs);
    printf("----------- end of regs ----------\n");
}

int main(){
   pid_t child;
   long orig_rax;
   child=fork();
   if(child==0){
      ptrace(PTRACE_TRACEME,0,NULL,NULL);
    //   execl("/home/v1me/workspace/hackergame2022-challenges/no_open/files/bin/chall",NULL,NULL);
      execl("/chall",NULL,NULL);
   }else{
        struct user_regs_struct regs, regs1;
        int i = 0;
        void *text_base = 0;

        wait(NULL);
        orig_rax = ptrace(PTRACE_PEEKUSER,child,8*ORIG_RAX,NULL);
        printf("orig_rax: %#llx\n",orig_rax);
        ptrace(PTRACE_GETREGS,child,NULL,&regs);
        printf("rip %#llx\n", regs.rip);
    

        while (1) {
            // ptrace(PTRACE_SYSCALL,child,NULL,NULL);
            ptrace(PTRACE_SYSCALL,child,NULL,NULL);
            wait(NULL);
            orig_rax = ptrace(PTRACE_PEEKUSER, child, 8 * ORIG_RAX, NULL);
            ptrace(PTRACE_GETREGS, child, NULL, &regs);
            // if (regs.rip < 0x555555554000 + 0x100000000000)
            
            if (orig_rax == SYS_mprotect && regs.rdi  / 0x100000000000 == 5) {
                printf("text_base: %#llx\n", regs.rdi-0x4000);
                break;
            } 
         }        
            text_base = regs.rdi-0x4000;
            printf("text_base: %#llx\n", text_base);


        while (1) {
            ptrace(PTRACE_SINGLESTEP,child,NULL,NULL);
            wait(NULL);
            ptrace(PTRACE_GETREGS, child, NULL, &regs);
            // if (regs.rip>=text_base && regs.rip<text_base+0x10000) {
                // print_regs(regs);
            // }
            if (regs.rip == text_base+0x1EF9) {
                print_regs(regs);
                memcpy(&regs1, &regs, sizeof(regs));
            }

            if (regs.rip == text_base+0x1F1B) {
                print_regs(regs);
                regs.rax = regs1.rax;
                regs.rdi = regs1.rdi;
                regs.rsi = text_base;
                regs.rdx = 0x6000;
                ptrace(PTRACE_SETREGS, child, NULL, &regs);
                break;
            }
            // if (orig_rax == SYS_read && regs.rdi == 3 && regs.rsi  / 0x100000000000 == 5) {
            //     printf("flag addr: %#llx\n", text_base+0x2020);
            //     uint64_t val =  ptrace(PTRACE_PEEKDATA, child, text_base+0x2020, NULL);
            //     printf("%#llx\n", &val);
            //     break;
            // } 
        }
   }
}
