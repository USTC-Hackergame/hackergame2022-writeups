# 置换魔群

题解作者：[tl2cents](https://github.com/tl2cents)

出题人、验题人、文案设计等：见 [Hackergame 2022 幕后工作人员](../../credits.pdf)。

## 题目描述

- 题目分类：math

- 题目分值：置换群上的 RSA（200）+ 置换群上的 DH（200）+ 置换群上的超大离散对数（300）

小 A 最近在鏖战密码学和代数学基础，密码学上有置乱和置乱阶，代数学基础老师又恰好讲了交错群（置换群） $A_n$：对 n 个元素的置乱操作。小 A 仔细一琢磨，这俩好像是一个玩意？之后代数学基础老师从置换群讲到最大的散在单群——魔群（monster group）与一个神奇的数——魔群的阶 M：808017424794512875886459904961710757005754368000000000，不仅牵扯到了傅里叶级数的展开系数，甚至还扯出了宇宙起源的弦论，也就是赫赫有名的“**魔群月光猜想**”。这时候，喜欢捣鼓物理的小 A 不淡定了，果然世界的终极本质还是数学，要好好研究一下群论了，就从置换群开始吧，毕竟任何一个群都能嵌入某个置换群。

小 A 首先把置换群的基本概念都烂熟于心，置换群的每一个元素都是一次置乱操作，比如

$$
A = \begin{bmatrix} 1 & 2 & 3 & 4 \newline 2 & 4 & 3 & 1 \end{bmatrix}
$$

上述置换代表着，位置 1 的元素经过置换后到位置 2，位置 2 的元素经过置换后到位置 4，位置 3 元素不变，位置 4 元素经过置换后到位置 1。其实上述置换由两个小置换构成： $A = (1 \rightarrow 2 \rightarrow 4 \rightarrow 1), (3 \rightarrow 3)$，标准化记为 $A=(1,2,4)(3)$，这就是 4 阶置换群 $A_4$ 上的一个 3 阶元素，因为连续经过三次 A 置换后，又复原了。置换群上的乘法运算 $A\*B$ 就是两次置乱的叠加：先用 B 进行置换，再进行 A 置换。如果 $A\_n$ 上的一个置换操作 A 至少要作用 k 次才能恢复到原状态（如 $A^3 = (1)(2)(3)(4)$ )，则 A 的阶是 k。

简单排列组合一下，小 A 发现 $A_n$ 置换群的阶是 $n!$，这可把小 A 高兴坏了，因为单单 $45!$ 可就比魔群的阶还要大得多了，这下小 A 有了一个大胆的想法，他要把魔群嵌入到某个交错群里，可是小 A 对这些代数结构的同构一窍不通，算了，管他呢，直接在某个置换群里面找一个阶为魔群的群的子群就行了，这很简单，找到最小的能包含阶为 M 的元素的置换群 $A_n$ 即可，小 A 准备把自己要找的群取名为**置换魔群**。

可是，小 A 发现，虽然可以找到置换魔群，但要表示这上面的一个元素，自己的磁盘空间远远不够，这可让他郁闷了好一阵，宇宙大概是个无限阶群吧，才会存在这么复杂的魔群。既然置换群这么神奇，小 A 决定在置换群上面做做公钥密码。

### 置换群上的 RSA

小 A 首先想到了著名的 RSA 算法，RSA 算法依赖的是给定 Zmod(n) 群，求该乘法群的阶的困难性，可是置换群 $A_n$ 的阶也太容易计算了吧，那就先送一道题练练手吧。

### 置换群上的 DH

既然 RSA 不行，小 A 决定研究一下置换群上的离散对数（DLP），置换群的阶可是随着 n 超指数级别增长，那么在这上面求解离散对数肯定是很困难的！小 A 于是仿照 DH 密钥交换协议，生成了自己的公私钥。你能破解他的私钥吗？

### 置换群上的超大离散对数

小 A 的私钥被破解了，他百思不得其解，怎么阶这么大的一个群，离散对数求解这么容易呢？肯定是自己实现有问题，于是决定把自己**私钥弄得比 $A_n$ 群上最大阶元素的阶还要大**，这样小 A 觉得万无一失了，甚至扬言，即使给黑客两次机会，他也拿不到我的私钥！可是一段时间后，小 A 的私钥又丢了。并且收到了黑客的留言：

> 置换群太**光滑**了，在这上面做传统的公钥密码，全是后门，毫无机密性可言，除非你能做到高阶的置换群，但是在此之前，你的内存肯定会炸掉。

### Hint

- 如果你对群论与魔群有兴趣，并且没有相关基础，这或许是一个很有用的视频：[群论与魔群](https://www.bilibili.com/video/BV1Rh411R7KL)
- 第三题：**怎么得到置乱群 $A_n$ 上的最大阶元素**，也就是怎么找到密码学意义上的最大置乱阶，并且构造**最乱的置换**。

### 题目连接以及附件

附件下载：[置换魔群附件](files/permutation_group.zip)

你可以通过 `nc 202.38.93.111 10114` 来连接，或者点击下面的 "打开/下载题目" 按钮通过网页终端与远程交互。

> 如果你不知道 `nc` 是什么，或者在使用上面的命令时遇到了困难，可以参考我们编写的 [萌新入门手册：如何使用 nc/ncat？](https://lug.ustc.edu.cn/planet/2019/09/how-to-use-nc/)



## 出题想法

置换群是结构很有趣的一个群， $A_n$ 的最大素数阶子群也就是 n 以内的最大素数，如果我们要构造求解离散对数困难的置换群 $A_n$，按照一般的安全性需要，n 必须要大于 $2^{160}$，想要无压缩的表示这个群上面的元素，需要至少 $2^{319}$ 比特，这导致一般可存储的置换群 $A_n$ 上的子群都是光滑的，也就是离散对数求解简单的，并且由于置换群的标准形式特别容易**看出来离散对数的解**（真"看出来"），用这个群来阐述光滑阶群的 `Pohlig Hellman` 离散对数求解算法就特别直观。所以这题前面两问有 CTF 经验的大手子们理解理解题意都能秒了，甚至熟悉 sage 接口的话，可以直接用 SageMath 上的 `SymmetricGroup/PermutationGroup` 类和 `discrete_log` 之类的轮子直接求离散对数，因为我自己用 Python 写的 `permutation_group` 类是直接仿照 `SymmetricGroup` 来写的，所以要改的地方几乎没有。写代码的时候把元素的 order 函数都写了，这样的话，第一题就完全是送分的题。

第三问算是开放式的一题，这一问的思路很清晰：找到两个 $A_n$ 上的元素，使得它们阶的最大公倍数最大 $MAX_{g_1,g_2 \in A_n} lcm(g_1.order(),g_2.order())$，如果只有一个元素，那就是求 $A_n$ 上的最大阶 $f(n)$，这个问题是有专门研究过的，称为 Landau's function，详细的研究可以参考 [A000793](http://oeis.org/A000793)，[Landau's function for one million billions](http://arxiv.org/abs/0803.2160)，当然，这个问题摊开来就是一个动态规划的问题（01 背包）。由于网上都有现成的脚本和结果，这里直接出单个元素形式的解法就可以 Google 做出来，所以放弃了这么出题。但是，如果扩展到两个元素，我在网上也没有找到确定性的研究结论，因此题目里面给的界只是出题人用贪心算法和动态规划求解出来的一个最大界（肯定不是理论上的最大上界），写 writeup 的时候又把这个界扩大了一点，如果谁研究出了更大的上界欢迎和我交流讨论。

附注：经过企鹅拼盘（这题用的就是 $A_{15}$ 交错群）出题人的提醒后发现题目文案有些数学上的不严谨，**全程提的都是置换群，而没有交错群**，交错群是置换群里面所有偶置换的形成的子群，元素个数为： $\frac{n!}{2}$；~~由于出题人没有全文替换之前写的置乱、交错等，导致部分叙述出现了交错群/置乱群~~， $A_n$一般表示交错群， $S_n, P_n$ 都可以用来表示该题的置换群。最后，感谢 zzh、djh、tky 等学长们对于本题出题的意见和帮助。



## 解题思路

第一题的 RSA，只要你对群的阶有一个基本的了解，这题就很简单了，我们加密了一个置换 g： $c = g^{e}$，类比 RSA，对应的私钥就很容易算了： $d = inverse(e,g.order())$，或者求 $e = 65537$ 模 $n!$ 的逆也可以，总之：


$$
c^d = g^{e*d} =g^{k*g.order()+1} = 1^k *g =g
$$


第二题就是求解离散对数了，本来想糊一个 DH 密钥的标准交换过程，最后还是直接搞 `dlp`。由于置换群的光滑性质，就可以直接用 sage 的 $discrete\\_log$ 出了（盲猜多数解法都会用 sage 的轮子直接跑了），由于置换群特别容易分解为不相关的子群（子置换），所以 `Pohlig Hellman` 光滑阶离散对数算法在置换群上特别直观，怎么自己写轮子参考第三节、代码参考纯 Python 写的 exp。

第三题其实是开放式的一题（~~因为出题人能力有限，找不到最大的上界orz~~），最后一节详细介绍了题目里最大阶的贪心构造方法，出题人写 writeup 的时候又想到了更直观的想法，求解两个元素联合起来的最大阶，只需要在不改变物品的情况下把原来背包问题的容量扩展到 $2n$ 即可，之后对阶 O 素因子分解得到的子集，求解一个 `approximate subset sum`，目标和为 $n$ ，由此得到两个 $O_1,O_2$ 作为两个生成元的阶，该方法比我之前得到的最大上界平均大了一个数量级（1~100 倍）。

纯 Python 解法（完善了 permutation group 类）参考 [python-exp](./python-exp/)，SageMath 脚本参考 [sage-exp](./sage-exp/)。



## 置换群上的 Pohlig Hellman 算法

我们首先来看 $A_5$ 上简单的例子， $A = (1,3)(2,4,5)$ ，对于位置不变的置换，我们将缺省，比如单位置换（不变置换）:  $A =(1)(2)(3)(4)(5)=()$ ，考虑 e = 1，2，3，4，5，6  


$$
\begin{align}
& A^1 = (1,3)(2,4,5) \\
& A^2 = (2,5,4)\\
& A^3 = (1,3) \\
& A^4 = (2,4,5)\\
& A^5 = (1,3)(2,5,4) \\
& A^6 = ()
\end{align}
$$


我们单独观察单个的小置换可以发现，(1,3) 的周期为 2，(2,4,5) 的周期为 3，所以 A 的阶是 6：

- 对于初始的 (1,3)，1 置换到 3， $A^2$ 置换就变成 1 置换 3 再置换到 1，也即是 1 置换到 1，周而复始；
- 对于初始的 (2,4,5)，2 置换到 4， $A^2$ 置换就变成 2 置换 4 再置换到 5，也就是 2 置换到 5， $A^3$ 就变成 2 置换到 2，周而复始。

因此，一般性的结论就是，我们考虑 $A$ 每个长度为 $l_i$ 小置换 $(x_1,x_2,...,x_{l_i})$ ， $A^e$ 结果为： $(x_1,x_j,...)$ ，则  $e\equiv j-1 \pmod{l_i}$ ，对于每个小置换我们都能得到这样一个式子，最后对所有关于 $l_i$ 的方程用中国剩余定理求解出来，我们就得到了 $e \bmod lcm(l_1,l_2,..,l_k) = order(g)$，也就是我们能够得到的关于 e 的最大的信息量了，如果  $e>order(g)$，我们是没法完全恢复出 e 的。

上面的方法也就是 `Pohlig Hellman` 算法的核心思想，不过在一般有限域 $Z_p$ 上面，子群（相当于 A 里面的小置换）是不好区分的，需要我们自己去构造。详细算法可以参考 [wiki](https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm)。

当然，由于题目里面的每个小子群的阶不超过 2000，因此直接对每一个小子群进行打表，计算下面的式子:

```python
[(e, sub_element**e) for sub_element in g.standard_tuple for e in range(len(sub_element))]
```

这样把结果里面的y对应的小置换直接查表得到对应的 e 即可，也就得到了 $x \equiv e\pmod{suborder}$。



## $A_n$ 上的最大阶元素（Two-Generator）

### Landau's function

考虑 $A_n$ 上一个置乱的阶，从互不相关小置乱的乘积的标准形式来看是最清晰的，我们只考虑小置乱的长度，记置乱 A 的长度数组为： $[l_1,l_2,..,l_k]$ ，那么求 $A_n$ 的最大置乱阶的问题就等价于下面问题（lcm：最大公倍数）：



$$
Landu(n) =Maxmize \quad lcm(l_1,l_2,...,l_k)\\
s.t. \quad \sum l_i = n, l_i,k \in Z^+
$$



最优解有下面两种性质几种情况： 

-   小置换长度 $l_i$ 不是素数的次幂之外的合数，否则 $l\_i = a\*b$ （非平凡分解），由于 $b^a,a^b\ge a\*b,a,b>=2$ 恒成立，并且在于其他数做 LCM 时， $a^b,b^a$ 之一的结果肯定不小于 $a\*b$ 的结果，因此最优解里面一定不存在上述合数。
-    $Landu(n)$ 一定可以表示为 $Landu(n)= MAX_{p^k \lt n} lcm(p^k,Landu(n-p^k))$ （最优子结构）

有了上面的结论就可以类似 01 背包问题愉快地动态规划了，背包的容量是 n，里面可以塞的东西就是小于 n 的所有素数次幂， $[p,p^2,..,p^k]$ 被归为一组，并且每一组内只能取一个元素。这样就可以用动态规划一次性解出所有小于等于 n 的最大阶。这是 [A000793](http://oeis.org/A000793) 上给出的 Python 动态规划代码：

```python
def aupton(N): # compute terms a(0)..a(N)
    V = [1 for j in range(N+1)]
    for i in primerange(2, N+1):
        for j in range(N, i-1, -1):
            hi = V[j]
            pp = i
            while pp <= j:
                hi = max((pp if j==pp else V[j-pp]*pp), hi)
                pp *= i
            V[j] = hi
    return V
```



### 贪婪策略

题目中上界的的生成方法，思路就是不管三七二十一，先产生 $A_n$ 上的一个最大阶为 $O_1$ 的元素 $g_1$ ，由于 $g_1$ 用到了 n 以内的某些素数、素数的次幂，所以我们第二次找最大阶元素的时候，需要重新更新一个物品（素数、素数次幂）的价值（权重），价值的更新策略如下：如果 $O_1$ 里面包含了素因子 $p^k$ （k 取最大的那个），那么:

-  $\forall\ i\le k：Value(p^i) = 1$
-  $\forall\ i\gt k：Value(p^i) = p^{i-k}$

更新物品价值后，再求解一次背包问题，得到第二个元素的最大阶 $O_2$ ，根据 $O_2$ 产生基底 $g_2$。纯粹的贪婪策略，最后为了防止直接分解这个上界得到泄露结果，最终的 bound 经过下面盲化处理：`bound = lcm(O1,O2) + randint(1, lcm(O1,O2)//100)`。连续通过 15 轮的概率是 $0.99^{15} \approx 0.87$。

代码如下（之前用 C 写的，抄过来有点丑）

```python
# sage 9.5
# For python you can use the `factorint` from sympy instead of `factor`
# from sympy import factorint
# factor = lambda x: list(factorint(x).items())
from math import sqrt,gcd
from Crypto.Util.number import *
from sympy import nextprime

def PrimeN(n):
    a = [0]*(n+1)
    a[0] = a[1] = 0
    for i  in range(2,n+1):
        a[i] = 1
    for i in range(2,int(sqrt(n)+1)):
        mul = 2
        if (a[i] == 0):
            continue
        while (i * mul <= n):
            a[i * mul] = 0
            mul+=1
    return a

def max_order_element_combine(n,nums=1):
    #MX = [1]*(n+1)
    prime = PrimeN(n)
    prime_pows = {}
    # init item values
    for i in range(n,-1,-1):
        if not prime[i]:continue
        k = i*i
        prime_pows.setdefault(i,i)
        while (k <= n):
            prime[i]+=1
            prime_pows.setdefault(k,k)
            k *= i
    res = [] # store the results
    for _ in range(nums):
        MX = [1]*(n+1)
        for i in range(2,n+1):
            if not prime[i]:continue
            for j in range(n,1,-1):
                temp = i
                for k in range(1,prime[i]+1):
                    if (j - temp >= 0 and MX[j] < MX[j - temp] * prime_pows[temp]):
                        MX[j] = MX[j - temp] * prime_pows[temp]
                    temp *= i
                    
        res.append(MX[-1])
        res_facts = factor(res[-1])
        # renew the item weights
        for f in res_facts:
            p_f =f[0]**f[1]
            j = f[0]
            while j < n:
                if j <= p_f:
                    prime_pows[j] = 1
                else:
                    prime_pows[j] = min(j//p_f,prime_pows[j])
                j*=f[0]
    return res
```



### 背包扩容策略

思路就是扩容背包，不扩大物品（素数幂）的选择范围；我们把背包容量扩大两倍，由此得到的最大阶 O 以及其标准素因子分解 $num\\_set = [p_1^{k_1},...,p_l^{k_l}]$，肯定有： $\sum_i p_i^{k^i} \le 2*$ 且 $\forall \ p_i^{k_i}\le n$ 成立。之后我们以 $num\\_set$ 为总的数集，以 $n$ 为目标和，求解最接近子集和问题，如果基于此对 $num\\_set$ 划分的两个子集和都小于等于 n，就可以构造符合条件的两个基底了。

``` python
# sage 9.5
# python version in python exp
def aupton_2(N): # compute terms a(0)..a(N)
    V = [1 for j in range(2*N+1)]
    for i in primerange(2, N+1):
        for j in range(2*N, i-1, -1):
            hi = V[j]
            pp = i
            while pp <= j:
                hi = max((pp if j==pp else V[j-pp]*pp), hi)
                pp *= i
            V[j] = hi
    return V
'''
Wikipedia subset sum approximation algorithm
http://en.wikipedia.org/wiki/Subset_sum_problem#Polynomial_time_approximate_algorithm
from https://github.com/saltycrane/subset-sum/blob/master/subsetsum/wikipedia.py
'''

import operator
def approx_with_accounting_and_duplicates(x_list,s):
    c = .01              # fraction error (constant)
    N = len(x_list)      # number of values

    S = [(0, [])]
    for x in sorted(x_list):
        T = []
        for y, y_list in S:
            T.append((x + y, y_list + [x]))
        U = T + S
        U = sorted(U, key=operator.itemgetter(0))
        y, y_list = U[0]
        S = [(y, y_list)]

        for z, z_list in U:
            lower_bound = (float(y) + c * float(s) / float(N))
            if lower_bound < z <= s:
                y = z
                S.append((z, z_list))

    return sort_by_col(S, 0)[-1]

def split_2n(n,order):
    num_set = set([p^e for p,e in factor(order)])
    target_sum = n
    sum1,prime_list1 = approx_with_accounting_and_duplicates(num_set,target_sum)
    prime_list2 = num_set - set(prime_list1)
    sum2 = sum(prime_list2)
    if sum1 <=  target_sum and sum2 <= target_sum:
        return prod(prime_list1),prod(prime_list2)
    
def Landu_expand(n):
    order = aupton_2(n)[-1]
    return split_2n(n,order)
```

