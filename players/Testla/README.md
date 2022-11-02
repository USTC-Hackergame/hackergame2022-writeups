# Hackergame 2022 Writeup

## 签到

开赛立马点开。看到 0 秒已经不指望能画出来了，打开开发者工具随便画画提交，发现就在 URL
query string 里。修改 URL 再次访问即可。

`flag{HappyHacking2022-<Redacted>}`

## 猫咪问答喵

1. <https://news.ustc.edu.cn/info/1047/28363.htm>

    > “星云战队”于2017年3月下旬组建成立

2. 打开 USTC LUG，新闻页面是
   [2022 秋季学期新生系列活动](https://lug.ustc.edu.cn/news/2022/09/2022-freshman-course/)
   ，底部有 PPT 链接，目标在第 15 页，菜单最下面就写着 Kdenlive。
3. 找到 <https://support.mozilla.org/en-US/questions/1052888>，楼主说是 28 也能用，结果错了，答案是回复里说的 12。
4. 打开 GitHub，搜索 argc，按 commit 日期排序，翻一下就能找到是
   [exec: Force single empty string when argv is empty](https://github.com/torvalds/linux/commit/dcd46d897adb70d63e025f175a00a89797d31a43)
   原漏洞印象挺深，导致我后来写 C 用 `argv[0]` 前都先判断一下，没想到 kernel 居然到三月才修。
5. 直接搜索会得到很多只匹配几个字节的结果，改用
   `"e4:ff:65:d7:be:5d:c8:44:1d:89:6b:50:f5:50:a0:ce"` 作为关键字后可以找到
   <https://docs.zeek.org/en/master/logs/ssh.html>，得到 IP 地址 205.166.94.16。
   直接用浏览器访问这个 IP 可以看到是 `sdf.org`，rDNS 都省了。话说“二级域名”这个
   叫法我一直没搞清楚，写题解时看了一下原来 Second-level domain 是指 TLD
   的下一级，感觉很多人把三级域名叫成二级域名。
6. 一开始找到 <https://netfee.ustc.edu.cn/faq/index.html#fee>，结果 2011-01-01
   不对。看到 <http://ustcnet.ustc.edu.cn/2010/1210/c11109a210869/page.htm>
   说原来也是一样的价格。进所在的“网字文件”往前翻找到
   <http://ustcnet.ustc.edu.cn/2003/0301/c11109a210890/page.htm>，得到
   2003-03-01。

另外今年能看到对了多少题了，能轻松确认答案对不对。

`flag{meowexamfullymeowed!_6c159adddb7f171b_<Redacted>}`

## 家目录里的秘密

先 grep 一下看看，得到第一个 flag。

```shell
$ grep -r "flag{"
.config/Code/User/History/2f23f721/DUGV.c:// flag{finding_everything_through_vscode_config_file_932rjdakd}
```

然后下载了 VSCode portable，把数据迁移过去一顿翻，无果。看 `.bash_history`
有配置过 rclone。打开 `.config/rclone/rclone.conf` 里面是一个 FTP 配置。复制配置用
rclone 连不上，我原来还以为 example.com 真的有 ftp 服务。那 flag 应该就是 FTP
密码了，想到抓包看，但感觉有点麻烦。发现有人发了
[golang 代码](https://forum.rclone.org/t/how-to-retrieve-a-crypt-password-from-a-config-file/20051)
，找个 playground 执行一下就行。

`flag{get_rclone_password_from_config!_2oi3dz1}`

## HeiLang

写个脚本把赋值拆开，然后执行。

`flag{6d9ad6e9a6268d96-<Redacted>}`

## Xcaptcha

一点按钮啪的一下就失败了，很快，题目都没看清。尝试禁用 JavaScript
后算出结果提交，会提示超时。用开发者工具看看代码，然后写个脚本来提交。

`flag{head1E55_br0w5er_and_ReQuEsTs_areallyour_FR1ENd_<Redacted>}`

## 旅行照片 2.0

第一题基本用 Windows explorer 就能完成。第二题搜索 `頂点を つかむ` 可以知道是 ZOZO
Marine Stadium，根据 EXIF 搜索 `xiaomi sm6115` 可以知道手机型号是 redmi 9，
像素不确定顺序两种都试试。

剩下最难的航班信息。首先根据地图镜头大致朝西，飞机机头向右，加上高度不高，
估计可能是羽田出发或者成田到达的飞机。然后一顿搜索，
两家机场官网最多只有当月的信息，<https://transtats.bts.gov/ONTIME/> 只有美国的航班，
没找到日本与之类似的网站，<https://opensky-network.org/> 需要注册，
还有很多需要付费的和需要同时填写两个机场的。archive.org 上的快照也很稀疏。有名的
flightradar24 老加载不出来。（还有就是当时 QQ 号没绑定手机不能登录，看不到群友讨论）
枚举了很多个在做题时时间接近的航班，又用了搜索引擎找 site:flightaware.com，全都不对，
就放弃了。

`flag{1f_y0u_d0NT_w4nt_shOw_theSe_th3n_w1Pe_EXlF}`

## 猜数字

看到随机数就想起去年 GeekGame 的
[扫雷](https://github.com/PKU-GeekGame/geekgame-1st/tree/master/writeups/liangjs#%E6%89%AB%E9%9B%B7)，
一看用的是 `java.security.SecureRandom`，那估计是没戏了（如果有应该会是大新闻）。
感觉服务器判断时加了延迟，而且规则也应该不会允许 1e6 规模的暴力。读了一下代码，
其他地方检查很足挑不出毛病，但判断相等时用的是
`var isPassed = !isLess && !isMore;`，就想到了 IEEE 754 NaN。提交时尝试删了
input 的 type 和 Event Listener 然后手动输入，还有
`document.getElementById("input").value = 'NaN'`，都不行。看了 HTML 里的
JavaScript 代码，改成 `range[1] = NaN` 就成功了。

`flag{gu3ss-n0t-a-numb3r-1nst3ad-<Redacted>}`

## LaTeX 机器人

搜索一下然后提交试试（

<https://www.wikitechy.com/tutorials/latex/input-vs-include-in-latex>

<https://tex.stackexchange.com/questions/3336/is-it-catcode-or-catcode>

```latex
\input{/flag1}
\catcode`\#=12 \catcode`\_=12 \input{/flag2}
```

`flag{becAr3fu11dUd3<Redacted>}`

`flag{latex_bec_0_m##es_co__#ol_<Redacted>}`

## Flag 的痕迹

页面很空，去找一个 Dokuwiki 网站乱点，然后把路径复制过来。

<http://202.38.93.111:15004/doku.php?id=start&do=diff>

`flag{d1gandFInD_d0kuw1k1_unexpectEd_API}`

## 安全的在线测评

静态数据直接 `system("cat ./data/static.out")` 就可以。

动态数据我一开始以为是考察怎么在多次被调用时保存状态，于是在文件系统中创建文件，
通过检查文件是否存在判断要读哪份输出数据。折腾了半天发现原来没有读权限，
而且在被调用时文件已经被关闭了。因为第一问的 flag 有提到编译器，而编译器的权限是跟 OJ
一样的，应该能读取到输出数据。一开始想的是用 `#include`，
发现如果不是数据配合是很难把内容直接存到字符串指针变量的。又搜索了一会找到神奇的
<https://github.com/graphitemaster/incbin>，复制下来用就可以了。

`flag{the_compiler_is_my_eyes_<Redacted>}`

`flag{cpp_need_P1040_std_embed_<Redacted>}`

## 线路板

下载 [gerbv](https://sourceforge.net/projects/gerbv)，打开文件，只保留
`ebaz_sdr-F_Cu.gbr`，选中并删除遮挡的圆圈就能看到了。

`flag{8_1ayER_rogeRS_81ind_V1a}`

## Flag 自动机

按钮会乱动点不到，tab 也不行，尝试了缩放和移动窗口甚至 AutoHotkey 都不行（那当然）。
用 Cheat Engine 看下内存，里面有 `flag_machine.txt` 字符串，附近写着
`Hint: You don't need to reverse the decryption logic itself.` 和私货
`Kanbe_Kotori`。用 Ghidra 打开，第一个函数就是判断是否成功的。乱操作一通 patch
成直接进入成功分支的样子，结果运行时只输出了一个加密后的 `flag_machine.txt`，
而且窗口关不掉……又读了
[相关文档](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nc-winuser-wndproc)
，知道这个函数是处理消息的，写个 AutoHotkey 脚本发一下就好。这里 0x1bf52 == 114514。

`flag{Y0u_rea1ly_kn0w_Win32API_89ab91ac0c}`

## 微积分计算小练习

先走一遍流程，然后看代码可以知道 flag 在 cookies 里，程序会提取并返回元素的内容。
观察成绩 URL，里面的 result 是分数 + ":" + 名字，所以就是要控制的这个
result 来修改元素了。先尝试了 `<script>`，发现通过 innerHTML 添加的不会被执行。
<https://ghinda.net/article/script-tags/> iframe 猜想读不到父页面的 cookies
没有尝试（后来看群发现是可以的）。看到可以用 `<img>` 的 onerror
<https://security.stackexchange.com/questions/60861>，在浏览器实验一下就成功了。

```HTML
<img src="/" onerror="document.getElementById('greeting').textContent = document.cookie;">:nobody
```

`flag{xS5_1OI_is_N0t_SOHARD_<Redacted>}`

## 杯窗鹅影

第一问很简单，直接 fopen 就行。

第二问先实验了一下，/flag2 没权限，/readflag 打印了头部是 ELF。这里犯了第一个错，
因为在 WSL 2 里也能运行编译生成的 PE 程序，就没有安装 Wine。一开始想用 execl，
在本地正常，上传就 ENOENT。改成内联汇编调用 execve 以免链接到奇怪的实现，还是不行
（目前对比答案生成的汇编，直接原因是传给 execve 的 pathname 字符串我存在全局
char[] 里，不在 .rdata 段上）。先 chdir 再用相对路径也不行。在本地装了 Wine
之后表现是一致了，但帮助不大。strace 直接看不到 execl 调用，看了前几天读过的
<https://werat.dev/blog/how-wine-works-101/> 像是被 Wine 处理了。然后尝试用
CreateProcess，也返回 no such file。一顿尝试之后用 `argv[0]` 的目录终于成功了。
实际上应该早点去看看 Wine 的文档。

`flag{Surprise_you_can_directory_traversal_1n_WINE_<Redacted>}`

`flag{W1ne_is_NeveR_a_SaNDB0x_<Redacted>}`

## 蒙特卡罗轮盘赌

用的随机数种子是略大于 `time(0)` 的，精度是 1 秒。修改程序往后打表，先随便猜两个就可以
grep 出来了。

`flag{raNd0m_nUmb34_a1wayS_m4tters_<Redacted>}`

## 惜字如金

第一问 HS384 的 secret 从 39 位 XZRJ 到了 11 位，需要补 28 位才能签名。
先算了一下可能的结果有 809999 个，于是决定暴力。这里主要是生成原 secret
的代码花了比较长时间才调好，运行时间倒只要几十秒。一个小坑是 sha384 后的 hash
XZRJ 后第一段结尾也可能有 e，不过这里算出来的没有。

第二问 n 是 768 位的，密钥要猜 21 * 5 = 105 位，目测没法暴力。

`flag{y0u-kn0w-h0w-t0-sav3-7h3-l3773rs-r1gh7-<Redacted>}`

## 不可加密的异世界

这道题自由度比较高，cipher 可以选 AES 或 DES，模式有四种可以选。

第一问明文后缀 14 字节已知，允许指定 key，要求 pad 之后加密后不变。
第二问明文直接随机 10 个 block，也是相似的要求。
一开始被 DES 吸引住了，因为看到四个
[Weak key](https://en.wikipedia.org/wiki/Weak_key#Weak_keys_in_DES) 各有
[2 ** 32 个不动点](https://crypto.stackexchange.com/questions/63423)，
如果找到一个 key 使得 Enc_key(0) = 0，配合 OFB 就可以秒杀前两问，可惜验证了都不是。

这时看到题目里加粗了“很短”，想到如果输入 1 字节长的前缀就可以保证 pad 之后刚好是
1 个 AES block。选 OFB mode，控制 cipher 输出全 0 就行，具体操作是随便选一个 key
用来 decrypt 0 得到 IV。

第二问读代码之后发现每次可以重新指定 key，而且只检查第 i 个 block。所以我们可以故技重施，控制第 i 个 block 的 cipher 输出全 0。

第三问要求加密两次后不变，很明显是 DES 的 Weak key 了。用作 key 的是输入 crc128
后的头部，所以我们要控制输入使这个 key 为 Weak key。

尝试从 crc128 结果倒推输入。crc 初始值确定，最终结果可以随便挑一个，27
行也比较好还原。问题在于 25 行的 `crc ^= b`，b 是自由的，但 crc
的约束在循环开始前的初始值那里，这就很难受。想到上次题解中看到的 z3，调了一会，
没跑多久就解出来了。反而是逻辑右移和数据类型的问题改了比较久。crc128
结果前八个字节后面的部分是自由的，代码里指定了全 0，因为也解出来了就不改了。

这题让我想起了 BEAST 和 EFAIL。用 block cipher 的时候最好还是选 AEAD
的模式，而且发现校验不通过就停止处理。

`flag{You_will_meet_a_softhearted_God_in_this_autumn_<Redacted>}`

`flag{Softhearted_God_is_a_ghost_always_on_call_<Redacted>}`

`flag{Harsh_God_also_releases_sunlight_in_winter_<Redacted>}`

## 置换魔群

第一问已知常数 `e` 和 `secret ** e`，求置换群 `secret`。因为对置换群来说
`secret ** secret.order() == secret`，所以我们只要求出 `x` 使得
`e * x == 1 (mod secret.order())`，算一下 `(secret ** e) ** x` 就得到 `secret`
了。虽然没学过数论，但搜索后可以知道要用扩展欧几里得算法，对着伪代码实现一份就行。

第二问换了个位置，已知置换群 `g` 和 `y = g ** secret`，求 `secret`。对 `g`
里的每一个小环（standard_tuple），它的周期是环的长度 `l`，只要查看 `y`
中对应元素的情况就可以知道 `secret % l` 的值。然后用中国剩余定理可以求出 `secret`，
因为 `secret` 的取值范围是 `[1, g.order()]` 所以是唯一的。

第三问是一个超大的 `secret`，我们有两次机会提供一个置换群 `g`，得到 `g ** secret`。
这需要我们构造 order 的最小公倍数尽可能大的两个交换群。一开始我是贪心取素数然后微调，
结果比上界少了 3 到 4 个数量级，还以为要暴力拼运气（。后来查了一下是
[Landau's function](https://en.wikipedia.org/wiki/Landau%27s_function)，
下载 [OEIS](https://oeis.org/A000793) 上的数列得到乘积，素因子分解一下就可以。
怎么分配成两组是个问题，我的做法是塞不下的时候将和减一再重试。

拿到 flag 之后想了一下，用动态规划可以算 Landau's function。

`flag{Pe5mRSA?__1s_s00oo_weak!!!_<Redacted>}`

`flag{p3mutat1on_gr0up_1s_smooth_dlp_easy_<Redacted>}`

`flag{choose_max_0rder_generator_l00k5_f1ne_<Redacted>}`

## 光与影

运行可以看到 flag 字样，而且播放时 GPU 占用率飙到 100%。
猜测应该是要把遮挡的白色矩形去掉。看到代码主要在 fragment-shader.js 里，没有混淆。
先全部保存到本地方便修改。看到代码里常数比较多的地方都在 t{1..5}SDF 这几个函数里，
其中 t5SDF 是最短的，设置 `t5 = 1e20` 就能看到 flag 了。

`flag{SDF-i3-FuN!}`

## 链上记忆大师

题目大意是按给定的 interface 实现一份合约，判题的合约会先调用 memorize 再调用
recall，要求返回原来的数据。

第一问按 solidity 官网的例子写写，然后编译提交就可以。

第二问判题的合约会在 memorize 后 revert。搜了一下 revert
之后绝大部分的改动都会被回滚，于是想尝试控制 gasleft。装 geth，杀掉残留进程，
生成新账户，改配置，然后创建合约的时候超时了。看了一下通过人数回去睡了。

`flag{Y0u_Ar3_n0w_f4M1l1ar_W1th_S0l1dity_st0rage_<Redacted>}`

## 片上系统

根据提示安装 PulseView，导入数据，按 metadata 里的值选 8 channels 16MHz，
可以看到只有前四个 channel 有活动，说明应该没错。添加一个 SD card SPI mode 的
decoder，按波形将四个 channel 分别设置为 CS、CLK、MOSI 和 MISO，就能看到数据了。
将第一块数据导出来还原就能看到 flag。

按题目提示，用
[在线 RISC-V 反汇编器](https://jborza.com/emulation/2021/04/18/riscv-disassembler.html)
反汇编第一个扇区。有些地方不太理解，但大致上是从 SD card 复制了 6 个扇区的内容到
0x20001000 开始的内存中。

后面的数据都是逐个字节传输的。先全部导出来观察，在开始和大概每隔一个扇区的位置都有一串
0xff，估计是 SD card 的协议。用 `dd skip=` 试出来偏移为 21 的时候可以反汇编。
反汇编结果比第一个扇区还令人困惑。因为在线反汇编器用了一些不标准的名字，在线的
simulator 跑不动。编译安装了
[riscv-gnu-toolchain](https://github.com/riscv-collab/riscv-gnu-toolchain)、
[spike](https://github.com/riscv-software-src/riscv-isa-sim) 和
[pk](https://github.com/riscv-software-src/riscv-pk)。
发现不是在线反汇编器的锅，只好运行看看。先转换成 ELF 格式还有
`riscv64-unknown-elf-objcopy --adjust-vma=0x20001000`
匹配下加载到的虚拟地址。一运行就 seg fault，调试了半天也没看懂。

写这份 writeup 的时候想起来，后面几个扇区前面的 0xff 忘记删了，偏移全都不对 233。

`flag{0K_you_goT_th3_b4sIc_1dE4_caRRy_0N}`

## 传达不到的文件

打开网页终端，藏有 flag 的两个文件确实没有权限。有 busybox，
好消息是有很多重要目录都有权限。`ldconfig -p` 看了一下，libc 确实可写，配合 suid
的 chall 可以为所欲为。但自己编译 libc 还是有点麻烦，而且也不知道 chall
调用了哪个函数，先试试 preload。复习一下 TLPI 42 章，`LD_PRELOAD` 确实对 suid
程序无效，但 `/etc/ld.so.preload` 可以。编译一个动态库，base64 上传，设置
preload 再运行 chall，就能拿到两个 flag。

```shell
gcc -shared -fPIC h.c -o h.so
base64 h.so
vi b
base64 -d b > h.so
echo /h.so > /etc/ld.so.preload
```

`flag{ptr4ce_m3_4nd_1_w1ll_4lways_b3_th3r3_f0r_u}`

`flag{D0_n0t_O0o0pen_me__unles5_u_tr4aced_my_p4th_<Redacted>}`

## 看不见的彼方

executor.c 里面列出了禁用的 syscall 列表，基本是 socket 相关的和 ptrace。
这样剩下还有很多可以用，打开 TLPI 看看有什么不需要访问路径的 IPC 方法，这里选了
System V message queue。

`flag{ChR00t_ISNOTFULL_1501AtiOn_<Redacted>}`

## 量子藏宝图

第一步是 BB84 量子密钥分发协议。先搜索一下，发现看不太懂，最后看下来感觉
[这个视频](https://youtu.be/44G9UuB2RWI)是说得最清晰的。其实很简单，有 + 和 x
两种选择（基底），分别都可以用一个光子传递 1 bit 的信息。
但当接收方使用的偏振片与光子偏振方向不是同一套时，
测量的结果会是不确定的（也就是不能用）。所以传输完光子之后双方公开使用的基底，
然后只保留相同的部分。简单起见可以发一长串 x 和一长串 0，数一下测量基底有多少个
x，密钥就是多少个 0。这里有个小坑是题目说只保留前 128 bit，但其实要输入整个密钥。

第二步是要根据量子电路图求出各个输出的值。观察发现每个量子会有 0 或 2 个同种类的
X 或者 Z gate，还可能异或到 q128。尝试发现只要有异或操作的 bit 就是 1，否则是 0。
手动抄下来解码就行。

`flag{<Redacted>}`

## 企鹅拼盘

第一问手动暴力，输入 1000 时可以通过。

第二问写程序暴力，原有的程序有点担心效率，还是自己写，结果还是很慢，大概 10/s。

第三问怎么说也不可能暴力 2 ** 64 了，因为看了一下前两问都只有唯一解。先把同一个
bit 上的操作合并起来，用置换魔群的代码分析一下置换群的样子，一看没什么特别。
可以分成两份 32 bit 然后从两边往中间暴力搜索，但是会爆内存而且运行时间也会很长。

`flag{it_works_like_magic_<Redacted>}`

`flag{Branching_Programs_are_NC1_<Redacted>}`

## 火眼金睛的小 E

先 `readelf -a` 看看那个地址的函数有多长，然后
`objdump -d --start-address= --stop-address=` 把那个函数反汇编出来。
`readelf -a | tail -n | sort -n -k 3` 看下长度比较接近的，全部反汇编出来，然后
vimdiff 肉眼看。

`flag{easy_to_use_bindiff_<Redacted>}`

## 部分没有通过的题目

### 二次元神经网络

以为考察神经网络，结果还真是 web，虽然也不一定做得出来。

### 你先别急

猜测是 SQL 注入，乱写了几个提交都是返回最高难度验证码，不知道怎么下手。

## 总结

第二次参加 Hackergame，题目还是新手友好且有趣。这次排名比上次高了不少，但
不可加密的异世界-严苛的神 和 传达不到的文件（届不到）感觉是运气好通过的，
置换魔群的数论入门算法也是靠临时抄。希望能继续提升，以后有机会再打。

注：杯窗鹅影 和 看不见的彼方 的部分代码使用了 Michael Kerrisk 写的
[The Linux Programming Interface](https://man7.org/tlpi/index.html) 中的
error_functions.h，可以在[这里](https://man7.org/tlpi/code/index.html)下载。
