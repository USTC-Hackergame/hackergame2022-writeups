from pwn import *

r = remote('202.38.93.111', 11451)

r.sendlineafter('Please input your token: ',
                '1:MEUCIQC24dB6B24/LDr2O+4cifbzOEFDbkXg3hJIqTXuuvpa1QIgbzMM/F0uUmYIudtM6qEDvOpEHbtTZjSjTWMcA5zhnos= ')

# until INIT OK
r.recvuntil('INIT OK')

with open('input.txt', 'r') as f:
    lines = f.readlines()

for l in lines:
    if len(l) > 2 and l[0] != '#':
        send = l.strip()
        recv = r.sendlineafter('>', send).decode()
        print(recv.strip())
        print(send)

recv = r.recvuntil('>').decode()
print(recv.strip())
