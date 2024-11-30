# 小 Z 的靓号钱包

题解作者：[mingliangz](https://github.com/mlzeng)

出题人、验题人、文案设计等：见 [Hackergame 2022 幕后工作人员](../../credits.pdf)。

## 题目描述

- 题目分类：math

- 题目分值：350

小 Z 最近听朋友说，有一家叫做 Wintermute 的交易公司，因为使用 [profanity](https://github.com/johguse/profanity) 生成了区块链上的靓号地址，[被盗](https://rekt.news/zh/wintermute-rekt-2/)了超过 1.6 亿美金。

「那真是太疯狂了！2018 年的时候，这个靓号生成工具还只有 **v1.12 版本**，我就用它生成了一个靓号地址 `0xffffffffffff0aa0914df1465327f33d591b30d8`，当时我用显卡跑了很久呢，没想到几年后大家才发现它不安全。」小 Z 感叹道。

他的朋友又跟他说，这个漏洞是随机数种子熵太小导致的，现在很多黑客和安全公司都已经实现了破解的算法，如果在链上有资金，要赶快提走。

小 Z 打开区块链浏览器，看了看自己在以太坊 Görli 测试网上的测试币。

「应该没有人会对我这点测试币感兴趣吧，何况旧版本的算法可能跟新版本的算法有一些区别，黑客应该没那么容易破解出我的私钥。」

提示：解决这个问题不需要很多计算资源（绝大多数办公笔记本电脑都是够用的）。

**[下载题目源代码](src/private_key_checker.py)**

你可以 `nc 202.38.93.111 10086` 来与远程交互，或者点击下面的 "打开/下载题目" 按钮通过网页终端与远程交互。

> 如果你不知道 `nc` 是什么，或者在使用上面的命令时遇到了困难，可以参考我们编写的 [萌新入门手册：如何使用 nc/ncat？](https://lug.ustc.edu.cn/planet/2019/09/how-to-use-nc/)

## 题解

这道题 idea 是 @zzh1996 的，我负责 implementation。

阅读 1inch Network 的[文章](https://blog.1inch.io/a-vulnerability-disclosed-in-profanity-an-ethereum-vanity-address-tool-68ed7455fc8c)可以了解破解 profanity 生成的靓号地址的私钥的原理（先**从交易签名中获取公钥**然后**中途相遇法计算私钥**）。具体实现细节也可以参考 Amber Group 的[文章](https://medium.com/amber-group/exploiting-the-profanity-flaw-e986576de7ab)。

### 获取公钥

使用区块链浏览器可以看到该地址在以太坊 Görli 测试网上面发过交易，获取交易哈希后，可以使用如下脚本从交易签名中恢复公钥。脚本代码实现参考了[链接](https://gist.github.com/CrackerHax/ec6964ea030d4b31d47b7d412036c623)。

```python
# Reference: https://gist.github.com/CrackerHax/ec6964ea030d4b31d47b7d412036c623

from web3 import Web3
from eth_account._utils.signing import to_standard_v, extract_chain_id, serializable_unsigned_transaction_from_dict

rpc_addr = 'https://ethereum-goerli-rpc.allthatnode.com'
tx_hash = '0x1032e388e1bae7fbdacb8ab5206abd3cf8f602736107b832de51bb10dac5e410'

w3 = Web3(Web3.HTTPProvider(rpc_addr))
tx = w3.eth.get_transaction(tx_hash)
s = w3.eth.account._keys.Signature(vrs=(to_standard_v(extract_chain_id(tx.v)[1]), w3.toInt(tx.r), w3.toInt(tx.s)))
tt = {k: tx[k] for k in ['chainId', 'nonce', 'gasPrice' if int(tx.type, 0) != 2 else '', 'gas', 'to', 'value',
                         'accessList', 'maxFeePerGas', 'maxPriorityFeePerGas'] if k in tx}
tt['data'] = tx['input']
ut = serializable_unsigned_transaction_from_dict(tt)
pk = s.recover_public_key_from_msg_hash(ut.hash())
print('pubkey:', str(pk).replace('0x', '0x04'))  # bitcoin uncompressed pubkey format
print('address:', pk.to_checksum_address())
```

运行脚本后得到公钥：

```
pubkey: 0x04a362925f16b3f45e7048b376dfd54beedee8defc8ea0804823c489f3cf5862f13e89da68fa280f0812ef2d339d95352bd97c03ccf0a6304a1aa004b6557ddd4b
address: 0xFFfFFfFFfFFf0aa0914DF1465327f33d591B30D8
```

### 计算私钥

通过阅读代码或者运行观察可以知道 profanity v1.12 版本枚举候选地址的方式：

* 使用 32bit 的真随机数初始化 `mt19937_64` 伪随机数生成器，并用其生成 256bit 的初始私钥。所以初始私钥只有 `2^32` 种可能性。（与最新版本一致）
* 枚举修改这个初始私钥的最高三字节（24bit），并计算出全部相应的地址和评分，打印评分高于以往最大值的地址。（与最新版本不同）
* 不断重复以上过程。（最新版本会递增初始私钥而不是重选初始私钥）

修改初始私钥对公钥产生的影响是增加 `x * (2^232) * G`（`G` 为生成元），其中 `x` 的取值范围是区间 `[-(2^24 - 1), (2^24 - 1)]` 之间的整数。因此小 Z 的公钥减去 `x * (2^232) * G` 得到的所有公钥中，必然有一个和某个初始私钥生成的公钥一样。所以将这些公钥存入哈希表，枚举所有 `2^32` 个初始私钥，计算对应公钥并查表即可。代码如下：

```c++
// Install bitcoin secp256k1 library (https://github.com/bitcoin-core/secp256k1)
// You can use command "sudo apt install libsecp256k1-dev" to install it on Ubuntu system

// Build piggypiggy secp256k1 library for fast enumeration (https://github.com/piggypiggy/secp256k1-x64)
// You can download the repo and use command "cd build && cmake .. && make" to build it on Ubuntu system

// Compile: g++ -O3 recover_key.cpp ./secp256k1-x64/bin/Release/libsecp256k1_x64.a -lsecp256k1 -fopenmp

#include <algorithm>
#include <iomanip>
#include <iostream>
#include <random>
#include <secp256k1.h>
#include <string>
#include <unordered_map>
#include <vector>

extern "C" {
#define P256_LIMBS 4
#define BN_ULONG unsigned long long
typedef struct {
  BN_ULONG X[P256_LIMBS];
  BN_ULONG Y[P256_LIMBS];
  BN_ULONG Z[P256_LIMBS];
} POINT256;
int CRYPTO_init();
int secp256k1_scalar_mul_gen(POINT256 *r, BN_ULONG scalar[P256_LIMBS]);
int secp256k1_point_get_affine(BN_ULONG x[P256_LIMBS], BN_ULONG y[P256_LIMBS],
                               const POINT256 *point);
}

int main() {
  std::unordered_map<uint64_t, int32_t> table;
  CRYPTO_init();
  secp256k1_context *ctx = secp256k1_context_create(SECP256K1_CONTEXT_VERIFY);
  std::string hex;
  std::cin >> hex;
  if (hex.substr(0, 2) == "0x") {
    hex = hex.substr(2);
  }
  {
    std::vector<unsigned char> bytes;
    for (size_t i = 0; i < hex.length(); i += 2) {
      bytes.push_back(std::stoul(hex.substr(i, 2), nullptr, 16));
    }
    secp256k1_pubkey pubkey;
    if (!secp256k1_ec_pubkey_parse(ctx, &pubkey, bytes.data(), bytes.size())) {
      std::cerr << "Invalid pubkey format" << std::endl;
      exit(1);
    }
    std::cerr << "Building table" << std::endl;
#pragma omp parallel for
    for (int32_t idx = -0xFFFFFF; idx <= 0xFFFFFF; idx++) {
      bool neg = idx < 0;
      int32_t idx_abs = neg ? -idx : idx;
      unsigned char tweak[32] = {idx_abs >> 16, idx_abs >> 8, idx_abs};
      secp256k1_pubkey temp = pubkey;
      if (!((!neg || secp256k1_ec_pubkey_negate(ctx, &temp)) &&
            secp256k1_ec_pubkey_tweak_add(ctx, &temp, tweak) &&
            (!neg || secp256k1_ec_pubkey_negate(ctx, &temp)))) {
#pragma omp critical
        {
          std::cerr << "Pubkey tweaking failed" << std::endl;
          exit(1);
        }
      }
      uint64_t hash = *(reinterpret_cast<uint64_t *>(temp.data));
#pragma omp critical
      {
        if (!table.insert({hash, idx}).second) {
          std::cerr << "Hash collision found" << std::endl;
          exit(1);
        }
      }
    }
  }
  {
    std::cerr << "Enumerating seeds" << std::endl;
#pragma omp parallel for
    for (uint64_t idx = 0; idx < (1ULL << 32); idx++) {
      std::mt19937_64 eng(idx);
      std::uniform_int_distribution<uint64_t> distr;
      BN_ULONG seckey[P256_LIMBS];
      for (size_t i = 0; i < 4; i++) {
        seckey[i] = distr(eng);
      }
      POINT256 point;
      BN_ULONG x[P256_LIMBS];
      BN_ULONG y[P256_LIMBS];
      secp256k1_scalar_mul_gen(&point, seckey);
      secp256k1_point_get_affine(x, y, &point);
      uint64_t hash = x[0];
      if (table.count(hash)) {
        seckey[3] -= (static_cast<int64_t>(table.at(hash)) << 40);
#pragma omp critical
        {
          std::cout << "0x";
          for (size_t i = 0; i < 4; i++) {
            std::cout << std::hex << std::setfill('0') << std::setw(16)
                      << seckey[3 - i];
          }
          std::cout << std::endl;
          exit(0);
        }
      }
    }
  }
}
```

编译运行，输入公钥，生成哈希表后，枚举一段时间即可得到私钥。在新款的办公笔记本电脑上进行测试，半个小时内可以得到结果。在 64 核服务器上进行测试，三分钟内可以得到结果。

## 出题思路

本节作者：[zzh1996](https://github.com/zzh1996)

这道题的出题思路是我提供的。

我很早就用过 Profanity 这个地址生成工具，2019 年 Hackergame 的[韭菜银行](https://github.com/ustclug/hackergame2019-writeups/blob/master/official/%E9%9F%AD%E8%8F%9C%E9%93%B6%E8%A1%8C/README.md)题目合约的[部署地址](https://kovan.etherscan.io/address/0x0000051935734850820502424350107413369555)还是用它生成的，我甚至给这个项目提过 [issue](https://github.com/johguse/profanity/issues/20)。

在这个漏洞被大规模利用之前，有一次我在 Flashbots 的 Discord 里面还看见过有人讨论年初的这个 [issue](https://github.com/johguse/profanity/issues/61)，我还在里面说用 BSGS 算法并且搞个 GPU 集群说不定可以破解出来，但是没有深入研究。没想到这个问题导致了如此严重的安全事件。

在漏洞爆出来后，很多研究机构和个人都实现了验证脚本。我跟 [mingliangz](https://github.com/mlzeng) 讨论能不能出成 Hackergame 题目，但是发现破解所需的计算量有点大，选手没有很强的机器可能跑不出来。除此之外，我们也担心比赛前或者比赛过程中有研究者在网上公开破解脚本。后来，mingliangz 发现旧版本破解所需的计算量会小很多，逻辑上还有一些不同使得针对最新版本的脚本没法直接使用，于是就出成了这道题。
