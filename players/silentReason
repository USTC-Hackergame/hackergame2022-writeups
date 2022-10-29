# Hackersgam2022 Writeup

​																			`silentReasonate`

## 签到

​	观察发现http://202.38.93.111:12022/?result=????明文发送，改为2022即可

## 猫咪问答喵

​	从GitHub、LUG、网络中心网站获取具体信息（commit、slide）；

​	搜索引擎和百科获取另外的题目其余二道；

​	域名通过1996年顶级域名只有com、net、org、edu、mil、ltd可以枚举前三位，sdf.org；

## 家目录里的秘密

​	VSCode打开文件夹，搜索pass字段，找到第一个flag在history中；

​	rclone经过搜索发现被obscure过，相应地执行rclone reveal即可；

## HeiLang

​	利用Python处理字符串，实现‘|’数组功能即可；

```python
def heIntelligenceAbility(inst):
    if inst.strip() == '':
        return
    content = int(inst.split('=')[1])
    addrs = inst.split('[')[1].split(']')[0].split('|')
    for addr in addrs:
        if addr.strip():
            a[int(addr.strip())] = content
```



## Xcaptcha

​	利用Python request，创建session，输入token后get网页内容，bs4解析后post即可

```python
import requests
import bs4

TOKEN = ""
session = requests.session()
session.get(TOKEN)

page = session.get("http://202.38.93.111:10047/xcaptcha")
soup = bs4.BeautifulSoup(page.content)

captcha = [eval(x.text.split(' ')[0]) for x in soup.find_all('label')]
payload = {"captcha" + str(i + 1): captcha[i] for i in range(0, len(captcha))}

page = session.post("http://202.38.93.111:10047/xcaptcha", data=payload)
answer = bs4.BeautifulSoup(page.content)
print(answer)
```



##  LaTeX机器人

​	利用catcode特性避免控制字符错误，同时利用“$$”截断，注入并include即可；

```latex
$$
\catcode `\$=12
\catcode `\#=12
\catcode `\_=12
\catcode `\&=12
$$
\include("/flag")
```

## 猜数字

​	利用Java的Double.NaN性质，网页端复制submit代码进行修改；

```javascript
guess.appendChild(document.createTextNode(parseFloat())) // NaN
```



## Flag的痕迹

​	去该wiki官网观察发现还有历史比较功能，发送&do=diff即可查看；

## 二次元神经网络

​	（失败解法）以为是利用神经网络特性进行图片压缩，观察第五个和第十个样本有连续色块，考虑初始训练时剔除，适当过拟合，再后续通过fine-tune嵌入，同时noise采用和eval是相同种子产生的固定值，很可惜成为了（0.001）的铁憨憨，本地最优时达到了0.008，可惜没能保存上传（还是过不了）。

## 安全的在线评测

​	静态文件比较简单，权限没限制，直接读取即可；

​	动态版本权限严格，但可以利用样例在编译前生成的弱点，利用利用asm的incbin特性构建external 指针，将外部文件嵌入，并在c中extern声明即可；

```assembly
	.global in#
    .type   in#, @object
    .balign 8
in#:
    .incbin "data/dynamic#.in"

	.global out1
    .type   out1, @object
    .balign 8
out#:
    .incbin "data/dynamic#.out"
```

## 线路板

​	利用`Altium Desiner`打开文件，但是没有编辑许可证，索性直接在文本编辑器中打开，试探删除部分内容，手动去除上方图层（注意不要破坏块结构），获得flag；

## Flag 自动机

​	利用Ghidra分析，找到更改按钮位置和判断管理员的函数，修补相关跳转语句逻辑条件即可；

## 微积分计算小练习

​	发现利用了innerHTML修改网页内容，同时atoi编码无过滤（但疑似有简单WAF）

​	selenium中会执行网页js，利用img的onerror自动延迟触发，将cookie写入#score中即可；

## 杯窗鹅影

​	读取文件操作直接前面添加‘/’即可，wine作为兼容层会自动处理识别；

​	执行这块由于将cmd和start删除了，没法直接启动，索性将wine源码中的program/start/start.c的代码移植过来用于辅助启动，手动用宏实现一些函数通过编译，然后利用start执行“/unix /readflag”即可；（非预期）

## 蒙特卡罗轮盘赌

​	根据unix时间戳和启动毫秒之和作为种子，故本地执行以下判断大致种子，枚举前后3000个可能值打表，利用网页中前两次结果查询即可逆推种子和后三次结果，从而得到具体答案；

## 光与影

​	将网页保存到本地，观察发现利用了SDF**函数进行了Glyph计算，同时利用min进行深度测试，观察后将t5删除即可；

## 不可加密的异世界

​	利用IV的XOR性质，第一问AES，其余两问主要利用DES弱密钥；

​	其中第三位利用XOR 0xFF使得CRC为0产生弱密钥（非预期），两次加密后保持不变；

## 置换魔群

​	利用置换群可以简单分解的特性，配合exCRT解决前两问，第三问构造尽可能多质数阶复合的轮换子列，同理可得；

## 传达不到的文件

​	while(true) do (sleep 100; /chall)& done

​	造成进程内存溢出被kill返回root shell（奇怪的非预期）

## 看不见的彼方

​	利用Linux共享内存机制，进程间添加一定等待时间即可；（非预期）

```c
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdio.h>

int main()
{
    FILE *fp = fopen("./secret", "r");
    char *secret = (char *)malloc(10000);
    fread(secret, 1, 10000, fp);
    fclose(fp);
    
    int shmid = shmget(0x1234, 10000, IPC_CREAT | 0666);
    char *shm = shmat(shmid, NULL, 0);
    memcpy(shm, secret, 10000);
    
    sleep(7);
    
    shmctl(shmid, IPC_RMID, NULL);
    return 0;    
}
```

```c
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdio.h>

int main()
{
    sleep(2);
    int shmid = shmget(0x1234, 10000, 0666);
    char *shm = shmat(shmid, NULL, 0);
    
    printf("%s", shm);
    return 0;
}
```



## 量子藏宝图

​	按照题意使用qiskit构建模拟量子电路输出结果即可；

## 《关于 RoboGame 的轮子永远调不准速度这件事》

​	利用rand种子确定且熵极小的特性，通过多字节写入调到预期随机数，读取0-Z即可；

## 企鹅拼盘

​	分析每次单步，观察到等价与一个16阶的置换，利用此性质去混淆；

​	观察分析发现相邻四个branch重复且组合后对应只有两种可能，利用该性质进行递归压缩，输出结果即可；

## 火眼金睛的小 E

​	利用objdump反汇编，endbr64确认函数入口，抽取相邻指令，配合fuzzwuzzy比较相似度可以解决前两问；
