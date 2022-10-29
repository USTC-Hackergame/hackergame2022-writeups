#include <windows.h>
#include <commctrl.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <stdbool.h>
#include <uxtheme.h>
#include "encryptor.h"

class anti_Debug
{
public:
    anti_Debug(void)
    {
        BOOL isDebuggerPresent = FALSE;
        if (CheckRemoteDebuggerPresent(GetCurrentProcess(), &isDebuggerPresent))
        {
            if (isDebuggerPresent)
            {
                exit(-1);
            }
        }
    }
};

#define ID_QUIT 2
#define ID_SELECT 3

// Simple anti dynamic debugging
anti_Debug nothing;
HWND button1_HWND = NULL;
HWND button2_HWND = NULL;
HWND prompt_HWND = NULL;

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg,
                         WPARAM wParam, LPARAM lParam)
{

    static wchar_t *prompt = L"您真的要从该软件中获取 flag 吗？";

    switch (msg)
    {
    case WM_CREATE:
        // 创建子窗口
        button1_HWND = CreateWindowW(L"Button", L"狠心夺取",
                                     WS_VISIBLE | WS_CHILD,
                                     85, 150, 80, 25, hwnd, (HMENU)ID_SELECT, NULL, NULL);

        button2_HWND = CreateWindowW(L"Button", L"放手离开",
                                     WS_VISIBLE | WS_CHILD,
                                     185, 150, 80, 25, hwnd, (HMENU)ID_QUIT, NULL, NULL);

        prompt_HWND = CreateWindowW(L"Static", prompt,
                                    WS_CHILD | WS_VISIBLE | SS_LEFT,
                                    85, 100, 300, 20, hwnd, (HMENU)1, NULL, NULL);

        // 禁用最大化按钮
        LONG style;
        style = GetWindowLong(hwnd, GWL_STYLE);
        style &= ~(WS_MAXIMIZEBOX);
        SetWindowLong(hwnd, GWL_STYLE, style);

        // 换字体
        HFONT hFont;

        hFont = CreateFontW(12,
                            0,
                            0,
                            0,
                            FW_REGULAR,
                            0,
                            0,
                            0,
                            GB2312_CHARSET,
                            OUT_DEFAULT_PRECIS,
                            CLIP_DEFAULT_PRECIS,
                            PROOF_QUALITY,
                            VARIABLE_PITCH | FF_ROMAN,
                            L"宋体");

        SendMessage(hwnd, WM_SETFONT, (WPARAM)hFont, TRUE);
        SendMessage(button1_HWND, WM_SETFONT, (WPARAM)hFont, TRUE);
        SendMessage(button2_HWND, WM_SETFONT, (WPARAM)hFont, TRUE);
        SendMessage(prompt_HWND, WM_SETFONT, (WPARAM)hFont, TRUE);

        break;

    case WM_COMMAND:
        if (LOWORD(wParam) == ID_QUIT)
        {
            PostQuitMessage(0);
        }

        if (LOWORD(wParam) == ID_SELECT)
        {
            if (lParam != 114514)
                MessageBoxW(hwnd, L"获取 flag 失败！您不是本机的 “超级管理员” ！", L"Error", 0);

            else
            {
                unsigned char *tmp = getflag(hwnd, lParam);

                MessageBoxW(hwnd, L"恭喜你获得 flag！flag 将保存到当前文件夹下的 flag_machine.txt 文件中！", L"Congratulations", 0);

                FILE *tmp_f = fopen("flag_machine.txt", "w");

                if (tmp_f == NULL)
                {
                    MessageBoxW(hwnd, L"文件打开错误！", L"Error", 0);
                    free(tmp);
                    exit(-1);
                }

                fwrite(tmp, 1, strlen((const char *)tmp), tmp_f);

                fclose(tmp_f);

                free(tmp);
            }
        }

        break;

    case WM_DESTROY:
        PostQuitMessage(0);
        break;
    }

    return DefWindowProcW(hwnd, msg, wParam, lParam);
}

LRESULT CALLBACK subWndProc(
    HWND hWnd,
    UINT uMsg,
    WPARAM wParam,
    LPARAM lParam,
    UINT_PTR uIdSubclass,
    DWORD_PTR dwRefData)
{
    switch (uMsg)
    {
    case WM_MOUSEMOVE:
    {
        int x = rand() % 150 + 50, y = rand() % 150 + 50;
        SetWindowPos(button1_HWND, HWND_TOP, x, y, 80, 25, (UINT)0);
        break;
    }
    }

    return DefSubclassProc(hWnd, uMsg, wParam, lParam);
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
                   LPSTR lpCmdLine, int nCmdShow)
{
    srand(time(0));

    WNDCLASSW wc = {0};
    wc.lpszClassName = L"flag 自动机";
    wc.hInstance = hInstance;
    wc.hbrBackground = GetSysColorBrush(COLOR_3DFACE);
    wc.lpfnWndProc = WndProc;
    wc.hCursor = LoadCursor(0, IDC_ARROW);

    RegisterClassW(&wc);
    CreateWindowW(wc.lpszClassName, L"flag 自动机",
                  WS_OVERLAPPEDWINDOW | WS_VISIBLE,
                  150, 150, 400, 300, 0, 0, hInstance, 0);

    SetWindowSubclass(button1_HWND, subWndProc, 400, 0);

    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return (int)msg.wParam;
}
