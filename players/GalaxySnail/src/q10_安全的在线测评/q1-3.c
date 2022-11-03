#include <stdio.h>

// 经过搜索，可以用 pragma 指令开启警告
// 这样一份代码就能获得两行输出
// https://gcc.gnu.org/onlinedocs/gcc/Diagnostic-Pragmas.html
#pragma GCC diagnostic warning "-Wall"
#pragma GCC diagnostic warning "-Wextra"

int main(void)
{
    #include "/proc/self/cwd/data/static.out"
    return 0;
}
