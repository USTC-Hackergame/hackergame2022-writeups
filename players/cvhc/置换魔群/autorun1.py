import re
import sys
from pwn import remote
from permutation_group import permutation_element

conn = remote("202.38.93.111", 10114)

conn.recvuntil(b'Please input your token: ')
conn.sendline(sys.argv[1].encode())

conn.recvuntil(b"> your choice: ")
conn.sendline(b"1")

for i in range(15):
    conn.recvuntil(b"[+] RSA public key: ")
    data = conn.recvline()
    n, e = [int(x) for x in re.findall(rb'\b\d+\b', data)]

    conn.recvuntil(b"[+] my encrypted secret is here: \n")
    data = conn.recvline()

    cipher = permutation_element(n, [int(i) for i in data[1:-2].split(b", ")])
    secret = cipher ** pow(e, -1, cipher.order())

    conn.sendline(str(secret).encode())
    conn.recvuntil(b"> your answer: Good job\n")

print(conn.recvline().decode())
conn.close()
