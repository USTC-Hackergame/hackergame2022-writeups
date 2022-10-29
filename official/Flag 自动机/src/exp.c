#include <windows.h>
#include <stdio.h>

int main(void){
    HWND target = NULL;

    // 获取窗口句柄
    target = FindWindowW(L"flag 自动机", L"flag 自动机");
    if (target == NULL){
        printf("error!");
        return -1;
    }
    printf("0x%x", target);

    // 发送消息
    PostMessageW(target, 0x111, 3, 114514);
    return 0;
}