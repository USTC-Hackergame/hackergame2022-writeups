# 惜字如金

题解作者：[ustc_zzzz](https://github.com/ustc-zzzz)

出题人、验题人、文案设计等：见 [Hackergame 2022 幕后工作人员](../../credits.pdf)。

## 题目描述

- 题目分类：math

- 题目分值：HS384（200）+ RS384（250）

惜字如金一向是程序开发的优良传统。无论是「[creat](https://stackoverflow.com/questions/8390979/why-create-system-call-is-called-creat)」还是「[referer](https://stackoverflow.com/questions/8226075/why-http-referer-is-single-r-not-http-referrer)」，都无不闪耀着程序员「节约每句话中的每一个字母」的优秀品质。本届信息安全大赛组委会决定贯彻落实这一精神，首次面向公众发布了「惜字如金化」（XZRJification）标准规范，现将该标准介绍如下。

### 惜字如金化标准

惜字如金化指的是将一串文本中的部分字符删除，从而形成另一串文本的过程。该标准针对的是文本中所有由 52 个拉丁字母连续排布形成的序列，在下文中统称为「单词」。一个单词中除「`AEIOUaeiou`」外的 42 个字母被称作「辅音字母」。整个惜字如金化的过程按照以下两条原则对文本中的每个单词进行操作：

- 第一原则（又称 creat 原则）：如单词最后一个字母为「`e`」或「`E`」，且该字母的上一个字母为辅音字母，则该字母予以删除。
- 第二原则（又称 referer 原则）：如单词中存在一串全部由完全相同（忽略大小写）的辅音字母组成的子串，则该子串仅保留第一个字母。

容易证明惜字如金化操作是幂等的：惜字如金化多次和惜字如金化一次的结果相同。

### 你的任务

我们为你提供了两个文件签名任务，分别称作 HS384 和 RS384。在每个任务中成功完成 3 次签名即可拿到对应 FLAG。

我们还为你提供了两个脚本方便你完成这两个任务——当然，这两个脚本已经被分别惜字如金化过了。

### 附注

本文已经过惜字如金化处理。

---

XIZIRUJIN has always been a good tradition of programing. Whether it is "[creat](https://stackoverflow.com/questions/8390979/why-create-system-call-is-called-creat)" or "[referer](https://stackoverflow.com/questions/8226075/why-http-referer-is-single-r-not-http-referrer)", they al shin with th great virtu of a programer which saves every leter in every sentens. Th Hackergam 2022 Comitee decided to inherit this spirit, and released th specification of "XZRJification" standard to th public for th first tim. W now introduc th standard as folows.

### XZRJification Standard

XZRJification refers to th proces of deleting som characters in a text which forms another text. Th standard aims at al th continuous sequences of 52 Latin leters named as "word"s in a text. Th 42 leters in a word except "`AEIOUaeiou`" ar caled "consonant"s. Th XZRJification proces operates on each word in th text acording to th folowing two principles:

- Th first principl (also known as creat principl): If th last leter of th word is "`e`" or "`E`", and th previous leter of this leter is a consonant, th leter wil b deleted.
- Th second principl (also known as referer principl): If ther is a substring of th sam consonant (ignoring cas) in a word, only th first leter of th substring wil b reserved.

It is easy to prov that XZRJification is idempotent: th result of procesing XZRJification multipl times is exactly th sam as that of only onc.

### Your Task

Ther ar two tasks named HS384 and RS384, which need you to generat signatures for files. Sucesfuly generating 3 signatures for each task wil lead you to th coresponding flag.

W also provid you with two scripts to help you complet thes two tasks - of cours, th two scripts hav been already procesed respectively through XZRJification.

### Notes

This articl has been procesed through XZRJification.

---

<p><b style="color:red">补充说明 1：在本题中没有大写字母因「惜字如金化」而被删除。<br/>
No capital leters in this chaleng hav been deleted due to "XZRJification".</b></p>

## 题解

题目描述里有一个「virtue」错打成「virtu」被眼尖的选手发现了，在此向这位选手表示感谢。

这道题我一开始想使用的编程语言是 Java，但由于我希望惜字如金后的源代码文件仍然是没有语法错误的文件，于是我在被 `class` 关键字难住后便转而去使用 Python 出题。各位选手应该能通过这道题提供的代码看出来一些试图这样做的痕迹，包括但不限于 `check_equals` 方法中使用 `exit`（因为 `raise` 和 `assert` 两个关键字都不行）、以及 `bool(0)` 的存在（不过实际上 `Fals` 只是一个不存在的变量，并不会带来语法错误）等。

### HS384

题目的第一问是用来带大家了解惜字如金这套机制是如何出题的。

首先我们看一眼 HS384 中的 HMAC Secret：

```py
# import secret
secret = b'ustc.edu.cn'
check_equals(len(secret), 39)
```

Secret 的长度明明是 11，怎么会是 39 呢——自然是有 28 个字符被惜字如金掉了。假设 Secret 全部为小写字母（当然我一开始并没有意识到需求额外增加这个假设，于是后面只能补公告，在此向补公告前试图解答此题的选手表达我的歉意），我们经过分析，能够得出 Secret 的可能形式是 `us(s*)t(t*)c(c*)(e?).ed(d*)u.c(c*)n(n*)`。接下来遍历所有可能的情况（约六十多万种）就可以了：

```py
#!/usr/bin/python3

import hashlib, re

possibilities = []

for e1 in [0, 1]:
  for e2 in [0, 1]:
    for s in range(e_subtracted := 28 - e1 - e2):
      for t in range(s_subtracted := e_subtracted - s):
        for c1 in range(t_subtracted := s_subtracted - t):
          for d in range(c1_subtracted := t_subtracted - c1):
            for c2 in range(d_subtracted := c1_subtracted - d):
              possibilities.append((s, t, c1, e1, d, c2, n := d_subtracted - c2, e2))

for s, t, c2, e1, d, c2, n, e2 in possibilities:
  key = f"us{s * 's'}t{t * 't'}c{c1 * 'c'}{e1 * 'e'}.ed{d * 'd'}u.c{c2 * 'c'}n{n * 'n'}{e2 * 'e'}"
  hash = re.sub('(?<=[a-f])e(?![a-f])', '', re.sub('([a-f])\\1*', '\\1', hashlib.sha384(key.encode()).hexdigest()))
  if hash == 'ec18f9dbc4aba825c7d4f9c726db1cb0d0babf47fa170f33d53bc62074271866a4e4d1325dc27f644fdad': print(key, hash)
```

解出 Secret 后直接使用该 Secret 签名即可。

附注：文件中 [`HS384-original.py`](src/HS384-original.py) 是 [`HS384.py`](src/HS384.py) 经惜字如金化处理前的文件。

### RS384

题目的第二问其实是 Coppersmith 方法的使用：把题目里的 `p` 和 `q` 猜出来。

通过对 RS384 的分析，我们可以得出：`p` 使用的是 32 进制编码，是通过遍历 `a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p.q.r.s.t.u.v.w.x.y.z` 使用 `.` 分隔后的短语列表生成的。`p` 在 32 进制下的长度是 77，从短语列表的第二个短语开始。为方便对应短语和数字，我们后面使用大写字母对应每个 32 进制的数。

我们可以得出 `p` 在 32 进制下的形式是：

```txt
p = BCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ # 32 进制
```

并且不难得出：

```txt
A = E = I = O = U = 31
```

我们立刻就能注意到 `p` 中有三段是重复的——换言之，我们可以定义 `x`、`a`、和 `b`，使其满足 `a * x + b = p`：

```txt
x = 0000000000000000000000000000000000000000000000000000BCDEFGHIJKLMNOPQRSTUVWXYZ # 32 进制

a = 2 ** 260 + 2 ** 130 + 1
  = 00000000000000000000000010000000000000000000000000100000000000000000000000001 # 32 进制

b = 31 * (2 ** 255 + 2 ** 125)
  = 0000000000000000000000000A0000000000000000000000000A0000000000000000000000000 # 32 进制
```

这里只有 `x` 是未知的，但 `x` 相较 `p` 而言又是非常小的数（数量级只约为 `p` 的三分之一）——这便是 Coppersmith 方法（[Coppersmith 相关攻击 - CTF Wiki](https://ctf-wiki.org/crypto/asymmetric/rsa/rsa_coppersmith_attack/)）的用武之地了。在本题中 `f(x) = x + (b * a⁻¹)` 为我们需要构造的多项式（`mod n`）。选手如果已经在自己的电脑上安装过 [SageMath](https://www.sagemath.org/) 的话，可以直接求解：

```sage
n = Integer(''.join(['255877945206268685758225801673342',
                     '992785361646269587137135214853754',
                     '886550982035142794210497165877879',
                     '580039847242541662956641303821238',
                     '094690165291113510002309824919965',
                     '575769641924765055087675446404464',
                     '357056205595528275052777855000807']))

a, b = 2 ** 260 + 2 ** 130 + 1, 31 * (2 ** 255 + 2 ** 125)
P.<x> = PolynomialRing(Zmod(n))
f = x + b * inverse_mod(a, n)

x0 = f.small_roots(beta=0.5)[0]
p = Integer(a * x0 + b)
print(p, n // p)
```

解出 `p` 和 `q` 后直接构造私钥签名即可。

附注：文件中 [`RS384-original.py`](src/RS384-original.py) 是 [`RS384.py`](src/RS384.py) 经惜字如金化处理前的文件。
