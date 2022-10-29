# 预期解及测试

`payload2-2.c` 是能拿到两个flag的预期解。

`payload1-1/2` 利用`#include`能拿到`static.out`中的数据，然后`payload1-3.c`输出拿到的数据即可得到flag1。

`payload2-1.c` 利用[INCBIN](https://github.com/graphitemaster/incbin)库（其实就是包装了`.incbin`汇编指令），在汇编阶段把文件内容嵌入到程序中，并定义为变量。`payload2-2.c`是经过`gcc -E` 预处理的`payload2-1.c`中的有用部分，只是减少了代码长度，不需要把整个`incbin.h`复制下来。代码把`dynamic[0-4].in`和`dynamic[0-4].out`的内容都生成为代码中的变量，然后跟输入对比，选择相应的输出输出即可。如果都不对，说明是静态数据。


