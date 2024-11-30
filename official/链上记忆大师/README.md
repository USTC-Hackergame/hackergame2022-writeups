# 链上记忆大师

题解作者：[zzh1996](https://github.com/zzh1996)

出题人、验题人、文案设计等：见 [Hackergame 2022 幕后工作人员](../../credits.pdf)。

## 题目描述

- 题目分类：general

- 题目分值：记忆练习（200）+ 牛刀小试（250）+ 终极挑战（250）

听说你在区块链上部署的智能合约有过目不忘的能力。

**[下载题目源代码](src/链上记忆大师.zip)**

你可以通过 `nc 202.38.93.111 10100` 来连接，或者点击下面的 "打开/下载题目" 按钮通过网页终端与远程交互。

> 如果你不知道 `nc` 是什么，或者在使用上面的命令时遇到了困难，可以参考我们编写的 [萌新入门手册：如何使用 nc/ncat？](https://lug.ustc.edu.cn/planet/2019/09/how-to-use-nc/)

## 题解

这题是我去年「[链上预言家](https://github.com/USTC-Hackergame/hackergame2021-writeups/blob/master/official/%E9%93%BE%E4%B8%8A%E9%A2%84%E8%A8%80%E5%AE%B6/README.md)」一题的续作。

### 记忆练习

第一问是送分题，用来给选手熟悉一下以太坊智能合约编译成字节码的流程，以及本题使用的框架。

题目合约内容是：

```solidity
pragma solidity =0.8.17;

interface MemoryMaster {
    function memorize(uint256 n) external;
    function recall() external view returns (uint256);
}

contract Challenge {
    function test(MemoryMaster m, uint256 n) external returns (bool) {
        m.memorize(n);
        uint256 recalled = m.recall();
        return recalled == n;
    }
}

```

我们需要写一个 `MemoryMaster` 合约，提供 `memorize(n)` 和 `recall()` 两个函数，第一个函数被调用时会传入一个 `n`，第二个函数被调用时返回刚才得到的 `n` 即可。第一问没有任何额外限制，直接用 Solidity 语言的变量（对应 EVM 的 Storage）存储即可：

```solidity
pragma solidity =0.8.17;

contract MemoryMaster {
    uint s;
    function memorize(uint256 n) external {
        s = n;
    }
    function recall() external returns (uint256){
        return s;
    }
}
```

至于如何把智能合约源代码编译成字节码，可以参考题目源代码中的编译脚本，也可以直接用在线的 [Remix IDE](https://remix.ethereum.org/)。在 Remix IDE 中编译后点击复制 Bytecode 的按钮，即可复制出一段包含字节码的 JSON。

### 牛刀小试

```solidity
pragma solidity =0.8.17;

interface MemoryMaster {
    function memorize(uint16 n) external;
    function recall() external view returns (uint16);
}

contract Challenge {
    function test(MemoryMaster m, uint16 n) external returns (bool) {
        try this.memorize_revert(m, n) {
        } catch (bytes memory) {
        }

        uint16 recalled = m.recall();
        return recalled == n;
    }

    function memorize_revert(MemoryMaster m, uint16 n) external {
        m.memorize(n);
        revert();
    }
}
```

这一小问相比上一个小问的区别是，`n` 的类型从 `uint256` 变成了 `uint16`，并且 `memorize` 函数执行完之后会被回滚。

EVM 中永久存储状态的变化会被回滚，所以这里没办法使用变量（对应 EVM 的 Storage）或者地址的余额等信息来记录 `n` 的值。我们可以想一想 EVM 中发生回滚的时候什么东西没有被回退到之前的状态，那就是 gas。在 EVM 中，gas 是对字节码执行过程中消耗的计算资源的测量，例如说一次加法会消耗 3 个 gas，一次乘法会消耗 5 个 gas，创建一个新合约要消耗至少几万个 gas。EVM 回滚的时候 gas 不会被回滚。（不然的话你岂不是白嫖了宝贵的计算资源！）

想了解 EVM 的一些细节可以参考[这个网站](https://www.evm.codes/)。

所以我们这里可以在 `memorize(n)` 函数中根据 `n` 的值来故意消耗不同数量的 gas，然后在 `recall()` 函数中获取一下当前剩余的 gas 即可得到之前遗留下来的信息。

但是，这个对应关系怎么确定？最差的方法是，对 65536 种情况分别进行测试，并且打一个表。但是，如果你对 EVM 比较了解，其实 gas 之间的关系很容易估算。

我们知道一些事实：

- 在 `memorize(n)` 函数中多消耗多少 gas，之后 gas 剩余量就会减少多少
- 在进入一层函数调用时，只有剩余 gas 的 63/64 会被传入
- 固定的代码执行消耗的 gas 一般来说比较固定
- 本题中对选手提交的合约测试是通过 `eth_call` 来测试的，而不是真的在链上产生交易，所以初始 gas 受到 geth 的 `--rpc.gascap` 参数控制，默认为 50000000。
- 合约调用的参数会消耗一些 gas，每一个非零字节是 16 gas，零字节是 4 gas，本题中只有 `n` 这个参数会变化，带来的影响可以忽略不计。

所以若 `memorize(n)` 函数中故意消耗 x gas，则 `recall()` 函数中剩余的 gas 应该大概是 `(50000000 - k - x) * 63 / 64` 这样，我们只需要测出来 `k` 就行了。（当然，懒着测的话也可以暴力枚举一下。）

（其实上面这些都不是必要的分析，你只要知道是线性相关就足够拟合出来了。）

我们可以估算一下，对于 50000000 的 gas 范围，切分成 65536 个区间，每个区间大小大概是 763 左右，由于考虑到函数调用只会传入 63/64 gas 的问题，以及其他固定代码执行消耗的 gas，我把区间大小取成了 700，也就是说 `memorize(n)` 函数中根据 `n` 来故意消耗 `n * 700` gas。

如果选手愿意在本地搭环境，那么调试 gas 的方法有很多，比如 `debug_traceCall` 这个 RPC 就可以输出每一条 EVM 指令执行时的 gas 情况。

这里提供一种不需要本地搭环境的取巧解法，即通过 revert 的信息把 gas 显示出来。revert 信息只能返回字符串，所以我在网上随便找了个整数转字符串的函数（也可以自己写）。

```solidity
pragma solidity =0.8.17;

contract MemoryMaster {
    function memorize(uint16 n) external view {
        uint g = gasleft();
        while (gasleft() > g - uint(n) * 700) gasleft();
    }
    function recall() external view returns (uint16){
        uint x = gasleft();
        revert(integerToString(x));
    }

    function integerToString(uint _i) public pure returns (string memory) {
        if (_i == 0) {
            return "0";
        }
        uint j = _i;
        uint len;
        while (j != 0) {
            len++;
            j /= 10;
        }
        bytes memory bstr = new bytes(len);
        uint k = len - 1;
        while (_i != 0) {
            bstr[k] = bytes1(uint8(48 + _i % 10));
            if (k > 0) k--;
            _i /= 10;
        }
        return string(bstr);
    }
}
```

提交字节码后，可以看到如下信息：

```
Testing 1/10...
n = 54232
...
web3.exceptions.ContractLogicError: execution reverted: 11819604
```

这样我们就知道了 `n = 54232` 时执行到 `recall()` 时剩余的 gas 是 11819604 了。注意这个结果可能跟你的编译器版本和优化参数有关，所以可能对你的情况不适用。

代入公式，由 `(50000000 - k - 54232 * 700) * 63 / 64 = 11819604` 解出 `k = 30384`。

于是写出最终的解题代码：

```solidity
pragma solidity =0.8.17;

contract MemoryMaster {
    function memorize(uint16 n) external view {
        uint g = gasleft();
        while (gasleft() > g - uint(n) * 700) gasleft();
    }
    function recall() external view returns (uint16){
        uint x = gasleft();
        return uint16((50000000 - 30384 - x / 63 * 64 + 350) / 700);
    }
}
```

其中 `+ 350` 是起到四舍五入的效果。

### 终极挑战

上一问不难想到答案，但是实现起来比较折腾。这一问是比较难想到，但是一旦想到实现起来比较容易。

题目合约：

```solidity
pragma solidity =0.8.17;

interface MemoryMaster {
    function memorize(uint256 n) external view;
    function recall() external view returns (uint256);
}

contract Challenge {
    function test(MemoryMaster m, uint256 n) external returns (bool) {
        m.memorize(n);
        uint256 recalled = m.recall();
        return recalled == n;
    }
}
```

这一问跟第一问的唯一区别是，`memorize` 函数被限制成了 `view`，也就是只读的函数。在 EVM 层面，调用 `view` 的函数意味着生成的指令是 `STATICCALL`，这种函数调用里面不能出现任何对永久存储状态的改变（包括读写 Storage、转账、创建合约、自毁等），否则会报错回滚。

如果仍然按照第二问的思路，通过 gas 这单一信道的信息，是不可能传输 256 bit 的整数的，因为 gas 的取值范围一共就只有那么大。

仔细阅读 EVM 相关资料或者代码可以发现，EVM 执行过程中会维护 `accessed_addresses` 和 `accessed_storage_keys` 数据结构（注意它与交易参数中的 Access List 不同），这是在 [EIP-2929](https://eips.ethereum.org/EIPS/eip-2929) 中定义的，并在去年的 Berlin 网络升级中启用（之后进行过一些修改）。

通俗地讲，就是 EVM 初次访问一些地址和存储单元的时候 gas 比较贵（“冷地址/存储”），而同一个交易内后续访问相同地址和存储单元的时候会比较便宜（“热地址/存储”）。这样做的意义是让 EVM 的 gas 更接近计算机处理相关指令的实际开销。由于多次访问的数据可以被缓存，所以后续访问不应该消耗太多 gas。

我们只要在 `memorize(n)` 函数中故意去访问一些地址或者存储，当 `recall()` 被调用的时候，就可以通过重新访问并且测量 gas 消耗的方式来探测这个地址或者存储是否之前被访问过。这里我们使用地址的余额来实现。要注意的一点是，EVM 中从 1 开始的一些地址（当前是 1~9）是预编译合约，它们在交易开始执行时会直接被当做“热地址”，所以没法用来传输信息。我这里直接把 0x100 作为起点。

在 [evm.codes](https://www.evm.codes/) 上查阅 `BALANCE` 指令，可以看到，访问“热地址”和“冷地址”的开销分别是 100 gas 和 2600 gas，我们用 1000 gas 作为分界线即可。

```solidity
pragma solidity =0.8.17;

contract MemoryMaster {
    uint constant base = 0x100;
    function memorize(uint256 n) external view {
        for (uint i = 0; i < 256; i++) {
            if ((n >> i) & 1 != 0) {
                uint x = address(uint160(base + i)).balance;
            }
        }
    }
    function recall() external view returns (uint256){
        uint n;
        for (uint i = 0; i < 256; i++) {
            uint start = gasleft();
            uint x = address(uint160(base + i)).balance;
            if (start - gasleft() < 1000) {
                n |= 1 << i;
            }
        }
        return n;
    }
}
```

把每个地址的余额是否被访问过分别作为 1 bit 信息，256 个地址就可以携带 256 bit 的信息，让我们可以在两个只读的函数之间传递 `n` 这个整数。

另外值得一提的是，地址和存储的“冷热”状态在 EVM 回滚的时候也会被一起回滚，所以这个方法没法用来解第二问。我是故意这样设计的。
