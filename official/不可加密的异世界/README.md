# 不可加密的异世界

题解作者：[tl2cents](https://github.com/tl2cents)

出题人、验题人、文案设计等：见 [Hackergame 2022 幕后工作人员](https://hack.lug.ustc.edu.cn/credits/)。

## 题目描述

- 题目分类：math

- 题目分值：疏忽的神（200）+ 心软的神（200）+ 严苛的神（250）

某节密码学导论课上，老师枯燥地讲着**对称加密算法**，而地心引力正诱惑着你上眼皮疯狂下坠，眼前的世界朦朦胧胧地在晃动的时候，你心想，要是这个世界没有加密算法该多好，什么 **Feistel** 结构、置乱、非线性运算通通不需要，万恶的加密掩盖了这世界的真实……终于你两眼一耷拉，进入了梦乡。

“旅行者，欢迎来到 Plain World！”

当你恍然苏醒过来，耳边传来了这一句话。看着周遭完全陌生的环境，你意识到自己好像穿越了。

“没错，某位神灵听见了你的心声，于是将你从混浊、满是秘密与猜忌的加密世界里转生到了无密的纯净世界，在这里，只有能让加密算法全部失效的智者才能得到最终的归宿，否则你将永远迷失。”

“在这里，你将接受三位神明的考验。”

虽然满脑子是问号，你还是跟随着这个声音的指引进入了这个不可加密的世界……

### 疏忽的神

你遇见了一个疏忽大意的神，他听到你的名字后，随意写了一个**很短**的通行证，说道：

“世事至繁，唯简为真；行路漫漫，虚名困身。”

这个神虽然恍恍惚惚没睡醒的样子，却还喜欢说一些故弄玄虚的话。但是看着他给出的考验，转念一想，好像还真是那么一回事，简单才是这个世界的本质。

一番折腾过后，你终于交出了令这位疏忽的神满意的答案，临别之际，他还念叨道：“希望你能遇见一位心软的神灵”。

### 心软的神

穿过一片片迷雾后，你居然真的遇见了一位心软的神，一见面就对你嘘寒问暖，得知你是异世界的来客后，还安慰了起来。

“异世界的来客，只身在此，你不必过于匆忙，旅途的意义在于其本身，而不是终点。**一步一步走**，终能达成所愿。”

虽然有些受不了这位神明过于泛滥的关心和善意，但你还遵循她的建议，一步一步完成这位神明的考验。随后，你走向了异世界的最终考验。

### 严苛的神

不知过了多久，你终于见到最后的这位神明，他面如寒霜，身姿挺拔，远见就有一种庄严的气势。

“根据法则，密钥的选择必须受限。”

随后，他又补充到：

“噢，对了，不管怎么，这次我要**多加密一次**。”

这位神明可真严苛，明明已经有一个限制，偏偏还要再加一条。

然而，真的是这样吗？你陷入了沉思.....

### 题目连接以及附件

附件下载：[不可加密的异世界附件](files/unencryptable_world.zip)

你可以通过 `nc 202.38.93.111 10110` 来连接题目，或者点击下面的 "打开/下载题目" 按钮通过网页终端与远程交互。

> 如果你不知道 `nc` 是什么，或者在使用上面的命令时遇到了困难，可以参考我们编写的 [萌新入门手册：如何使用 nc/ncat？](https://lug.ustc.edu.cn/planet/2019/09/how-to-use-nc/)



## 题解

这题的出题的思路就是通过一些小 trick 使得加密后的密文与明文相同。

前面两道题的预期解都是利用 CBC 模式下的 IV 的冗余，不需要任何爆破，就可以指定任意一个密文分组的值为我们预期的值，详情参考下一节“**CBC 模式指定任意密文分组**”。

最后一问，题目已经很明显地用了两个密码学上已经破解的算法，所有也很容易往 DES 和 CRC 想到这两个点：crc 类哈希都是可逆的以及 DES 的弱密钥；DES 也就是为了第三问加进来的，AES 是目前最流行的对称加密体制，没有任何已知的有效攻击；而 DES 是存在诸多问题的，差分攻击、彩虹表、弱密钥等等。而最后一问我们是要求**加密两次**恢复到原明文，这比加密一次恢复到原明文的条件更弱，因此只要使用 DES 的弱密钥（在 Feistel 结构下可以直接用弱密钥作为加密过程的密钥实现解密过程，不需要逆序使用子密钥），就可以两次加密（实际上等价于加密+解密）恢复明文。由于 crc 哈希是可逆的（见下下节），我们就可以直接把一个 DES 弱密钥当哈希逆向得到我们的消息，提交该消息即可。

完整题解和 exp 见附件 [unencryptable-exp.ipynb](./unencryptable-exp.ipynb)。（GitHub 的 LaTeX 数学公式支持可能出问题，也可以看 notebook 的题解）。最后感谢 zzh 学长对于本题非预期解法的修复。



## CBC 模式指定任意密文分组

CBC 模式的字节反转攻击算是 CTF 中老生常谈的考点了，这里也是稍微利用了一下 CBC 的模式特征：
![image.png](./CBC_encryption.svg.png)

如果在 CBC 分组加密模式下，我们可以选择 IV 并且已知 Key 的值的话，那么 IV 这 16 个字节的冗余可以转移到任意一个密文分组：也就是说我们可以任意指定一个密文分组的值，从而反推出所有密文分组的值以及 IV 的值。特别地，当明文长度就是一个分组时，我们可以控制整个密文的值。原理如下，假设我们指定密文分组 $C_i$ 为原来的明文 $m_i$：

-  $C_{i}$ 之后的密文：按 CBC 模式加密即可，初始 IV 就是 $C_i$，密钥为 Key（这部分按标准 CBC 加密即可）。
-  $C_{i}$ 之前的密文： $C_{i-1} = Dec(C_i) \oplus M_i$，以此类推，直到 IV 的值确定。

第一问根据提示，我们只要控制明文长度不超过 16 字节即可，因此随便输入单个字母，然后往前面推一步，就得到了 IV 值，第二问就是第一问的一个拓展，我们每次指定一个分组加密后为明文即可，主要的攻击代码写出来如下：

``` python
from Crypto.Util.number import *
from Crypto.Cipher import AES
import os

block_size=16
key_size=16

def pad(msg:bytes,block_size = 16):
    n = AES.block_size - len(msg) % AES.block_size
    return msg + bytes([n]) * n

def unpad(msg, block_size = 16):
    return msg[: -msg[-1]]

def xor(b1:bytes, b2:bytes):
    return bytes([x ^^ y for x, y in zip(b1, b2)])

def split_block(text:bytes):
    assert len(text)%block_size==0,'Invalid length'
    return [text[i*block_size:(i+1)*block_size] for i in range(len(text)//block_size)]

def AES_CBC_chosen_ciphertext(AES_key:bytes,plaintext:bytes,chosen_ciphertext:bytes,pos=None):
    # pos = None the iv will be set as chosen ciphertext
    # pos = -1 : the last block will be set as ciphertext
    # pos = i : the ith (from 0) block will be set as ciphertext    
    if pos==None:
        iv=chosen_ciphertext
        aes_cbc=AES.new(AES_key,AES.MODE_CBC,iv)
        return iv,aes_cbc.encrypt(msg)
    
    iv=os.urandom(block_size)
    aes_cbc=AES.new(AES_key,AES.MODE_CBC,iv)
    aes_ecb=AES.new(AES_key,AES.MODE_ECB)
    cipher=aes_cbc.encrypt(msg)
    msg_blocks=split_block(msg)
    cipher_blocks=split_block(cipher)
    cipher_blocks[pos]=chosen_ciphertext
    
    for i in range(pos-1,-1,-1):
        cipher_blocks[i]=xor(aes_ecb.decrypt(cipher_blocks[i+1]),msg_blocks[i+1])
    
    iv=xor(aes_ecb.decrypt(cipher_blocks[0]),msg_blocks[0])
    
    for i in range(pos+1,len(cipher_blocks)):
        cipher_blocks[i]=aes_ecb.encrypt(xor(cipher_blocks[i-1],msg_blocks[i]))
    
    return iv, b"".join(cipher_blocks)
```



## 逆 CRC128 哈希

Hacker Game 之前也出过 `crc128` 类似的题：[2020 年的题目「中间人」](https://github.com/USTC-Hackergame/hackergame2020-writeups/tree/master/official/%E4%B8%AD%E9%97%B4%E4%BA%BA)，更进一步可以找到 TCTF 的这道题：[fixed point](https://hxp.io/blog/51/0CTF-Quals-2019-fixed-point-writeup/)。无一例外，它们都利用了 crc128 的仿射函数性质：Affine Function in $GF(2^{128})$，其中 TCTF 这题的 writeup 还介绍了基于多项式的 crc 的表示方式，这个方式也可以直接求逆，这里介绍另外一种用矩阵的方式写出 crc 的表达式。crc 仿射函数最容易验证的性质就是： $crc(\Delta \oplus a)\oplus crc(\Delta \oplus  b) = \textrm{const}\quad  \forall \Delta$。也就是说只要两个明文的差分是一样的，那么它们 crc 哈希后的差分就是一个固定值。这个固定值是可以写出来的，定义 $\\_crc(x) = crc(x) \oplus crc(0^l)$，其中 $0^l$ 代表与 x 等长的 `"\x00"` 字节流。对于任意**等长的输入**就有:  


$$
\\_crc(\Delta \oplus a)\oplus \\_crc(\Delta \oplus  b) = \\_crc(a \oplus b)
$$

$$
\begin{align}
\textrm{Generally} \implies \forall x_i, n \quad \oplus_1^n \\_crc(x_i) =  \\_crc(\oplus_1^n x_i)
\end{align}
$$



其中 $\oplus$ 等价于 $GF(2)^{k}(\forall k \in Z)$ 上的加法，所以上式在 $GF(2)$ 上可记为：

$$
\forall x_i \in GF(2)^l, l \in Z ,n \in Z\quad \sum\limits_1^{n} \\_crc(x_i) =  \\_crc(\sum\limits_1^{n} x_i)  \quad + \textrm{defined in} \ GF(2)^k
$$


有了这个性质，对于 $GF(2)$ 上的 128 维的向量空间，取一组基底如下： $v_i = (0,..,1,...,0)\quad i \in \{1,2,3,...,128\}$，第 i 个位置为 1 其余均为 0 的标准正交基。我们记这一组标准正交基的 _crc 哈希值的对应的向量为， $V_i =\\_crc(v_i) \quad i \in \{1,2,3,...,128\}$，用 $V_i$ 构建一个在 $GF(2)$ 上的 128×128 的矩阵：


$$
\textrm{let} \quad M^T = \begin{bmatrix} 
V_1 \\
V_2 \\
...\\
V_{128}
\end{bmatrix} ,  
\forall \vec x =(x_1,...,x_n) \in GF(2)^{128}
$$

$$
\implies \ x*M^T = \sum\limits_{i=0}^{128} x_iV_i 
= \\_crc(\sum x_i*v_i)
= \\_crc(x) = crc(x) + crc(0^{128}) \in GF(2)^{128}
$$



从上面我们就得到了**定长**为 128 比特的输入做 crc 哈希时在 $GF(2)$ 上的等价矩阵表示（Affine Function）（其他长度的输入换一下矩阵 M 和 $crc(0^l)$ 的值即可），为了和代码保持一致，我们把 $M^T$ 再转置回来： 

$$
crc(x) = x*M^T + crc(0^{128}) \implies 
crc(x)^T = M*x^T + C \quad \textrm{where} \ C =   crc(0^{128})^T
$$


有了上面的矩阵表示，给定 crc128 的值，求它对应的一个明文，只需要解一个在 GF(2) 上的方程组即可 $x^T = M^{-1}*(crc(x)^T+C)$，这样我们就实现了一个完整的 `crc_128_reverse` 函数，这是最基础版本的推导，但是解决这题就够用了。一个简单的 sage demo 如下：

``` python
def crc128(data, poly=0x883ddfe55bba9af41f47bd6e0b0d8f8f):
    crc = (1 << 128) - 1
    for b in data:
        crc ^^= b
        for _ in range(8):
            crc = (crc >> 1) ^^ (poly & -(crc & 1))
    return crc ^^ ((1 << 128) - 1)

def equivalent_affine_crc(crc = crc128, crc_bits = 128, target_bytes = 16):
    zero_crc = crc(target_bytes*b"\x00")
    target_bits = 8 * target_bytes
    v2n = lambda v: int(''.join(map(str, v)), 2)
    n2v = lambda n: vector(GF(2), bin(n)[2:].zfill(crc_bits))
    # n2v_t = lambda n: vector(GF(2), bin(n)[2:].zfill(target_bits))
    Affine_Matrix = []
    for i in range(target_bits):
        v = vector(GF(2), (j == i for j in range(target_bits)))
        value = crc(long_to_bytes(v2n(v),target_bytes)) ^^ zero_crc
        Affine_Matrix.append(n2v(value))
    # crc affine function: crc_128(x) = M*x+ C
    return matrix(GF(2),Affine_Matrix).transpose(), n2v(zero_crc)

def crc_128_reverse(crc_value):
    M , C = equivalent_affine_crc()
    # crc affine function: crc_128(x) = M*x+ C
    v2n = lambda v: int(''.join(map(str, v)), 2)
    n2v = lambda n: vector(GF(2), bin(n)[2:].zfill(128))
    res = M.solve_right(n2v(crc_value)+C)
    return long_to_bytes(v2n(res),16)
```
