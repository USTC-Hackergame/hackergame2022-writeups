import pathlib
from pwn import *
import requests
import re
import subprocess
from concurrent.futures import ProcessPoolExecutor

context.log_level = 'debug'

dry_run = False

p = remote('localhost', 12400)
p.recvuntil(b'Please input your token:')
# p.sendline(b'22:MEUCIQD5Hla3DWFA1sTgYSNcdMjB2fYxc4fSUc9qnOynJXNwlgIgb3LSgzDDNQ3L1XFddZZk9Vmn74KQjGs7vIUe8YTFRik=')
p.sendline(b'1:MEQCIBxs4yBzfjnYS/o+Z3Bm3lJpIZVfvB1dsjSkzcgj8PakAiAtZcKG6tBqDhbOYEXwigMCd6bUBJe7P9KlIr6dxDPu4A==')

p.recvuntil(b'Choose your difficulty')
p.sendline(b'3')

p.recvuntil(b'Do you want to perform dry run, so that you can see how many challenges you can answer correctly? (y/N)')
p.sendline(b'y' if dry_run else b'N')

with open('latest_timestamp', 'r') as f:
    latest_timestamp = int(f.read())

p.recvuntil(b'Please input the timestamp: ')
p.sendline(str(latest_timestamp).encode())

problem_no = 0
problem_num = 1

save_dir = pathlib.Path('./problem-save')
save_dir.mkdir(exist_ok=True)

error_count = 0

zero_submit = 0

while problem_no < problem_num:
    p.recvuntil(b'Challenge')
    problem_no = int(p.recvuntil(b'of', drop=True).strip())
    problem_num = int(p.recvuntil(b'\n', drop=True).strip())

    # log.info(f'Challenge {problem_no} of {problem_num}')
    p.recvuntil(b'1st binary: ')
    src_url = p.recvuntil(b'\n', drop=True).strip().decode()
    # log.info(f'src: {src_url}')

    p.recvuntil(b'2nd binary: ')
    dst_url = p.recvuntil(b'\n', drop=True).strip().decode()
    # log.info(f'dst: {dst_url}')

    p.recvuntil(b'There is a function at ')
    target_addr = int(p.recvuntil(b' ', drop=True).strip().decode(), 16)

    cur_problem_save_dir = save_dir / f'problem-{problem_no}'
    cur_problem_save_dir.mkdir(exist_ok=True)

    try:
        with (cur_problem_save_dir / 'safe_dst_target_addr').open('r') as f:
            dst_target_addr = int(f.read().strip(), 16)
    except Exception as e:
        print(e)
        dst_target_addr = 0
    # print(hex(dst_target_addr))

    p.sendline(hex(dst_target_addr).encode())

    if dst_target_addr == 0:
        zero_submit += 1


    if dry_run:
        p.recvuntil(b'real pair:')
        src_addr_by_nc = int(p.recvuntil(
            b'->', drop=True).strip().decode(), 16)
        dst_addr_by_nc = int(p.recvuntil(
            b'\n', drop=True).strip().decode(), 16)

        with open(cur_problem_save_dir / 'real_addr', 'w') as f:
            f.write(hex(dst_addr_by_nc))

        if dst_addr_by_nc != dst_target_addr:
            error_count += 1

            print(
                f'problem {problem_no} error, target: {hex(target_addr)}, submit: {hex(dst_target_addr)}, real: {hex(dst_addr_by_nc)}')

if dry_run:
    print(f'error count: {error_count}')

print(zero_submit)

p.interactive()
