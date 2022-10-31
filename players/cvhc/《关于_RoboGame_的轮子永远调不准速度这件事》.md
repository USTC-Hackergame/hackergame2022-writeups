## 《关于 RoboGame 的轮子永远调不准速度这件事》

那个 `firmware.c` 功能非常清楚。每次写第 `i` 个 port，第 `(i+1)%10` 和 `(i-1)%10` 个 port 都会被写入 `rand()` 函数产生的“随机”数据。

跑一下这个 `rand()` 函数，会发现返回的数字是以8为周期循环的：`11, 45, 14, 19, 81, 24, 00, 19`（十六进制）。具体到个别数字，每4次调用就会得到一次 `0x19`。

然后在测试环境下可以看出，往某个 port 写多个字节，只有第一个字节影响轮子转速。解题方法就很明显了： `rand()` 返回前三个值后，我们只要接着每次写4个字节，就能始终得到 `0x19` 的“随机”转速。

另外，在测试环境下还可以得到，前10个轮子转速的初始值是 `11, 45, 14, 19, 19, 81, 00, 45`（十六进制），轮子 4/5 的转速已经是 `0x19`。所以只需要用上述方法把剩下8个轮子转速调成 `0x19`，10次调速绰绰有余。

调速输入如下：

```
w 0 3 0 0 0      # 跳过前三个 rand() 返回值
w 1 4 25 0 0 0   # 调整 0, 1, 2 号轮（转速是十进制）
w 6 4 25 0 0 0   # 调整 5, 6, 7 号轮
w 9 4 25 0 0 0   # 调整 8, 9, 0 号轮
```

另外附上完整的自动读 flag 的代码：

```python
import sys
from pwn import remote

conn = remote("202.38.93.111", 11451)

conn.recvuntil(b'Please input your token: ')
conn.sendline(sys.argv[1].encode())
conn.recvuntil(b"INIT OK")

conn.sendline(b"w 0 3 0 0 0")
conn.sendline(b"w 1 4 25 0 0 0")
conn.sendline(b"w 6 4 25 0 0 0")
conn.sendline(b"w 9 4 25 0 0 0")
conn.recvuntil(b"Congrats! Flag is in the speed data of all wheels.")

r_cmd = bytearray(b"r _ 1")
out_buffer = bytearray()

for i in range(0x24):
    conn.recvuntil(b"> ")

    r_cmd[2] = ord('0') + i
    conn.sendline(r_cmd)
    conn.recvuntil(b"i2c status: transaction completed / ready\n")

    byte = int(conn.recvline()[:2], 16)
    out_buffer.append(byte)

print(out_buffer.decode())
```

