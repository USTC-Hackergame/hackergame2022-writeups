## Flag 自动机

没有 IDA 只会 `objdump` 的选手来献丑了。

### 点不到的按钮

这个我会，写个自动化脚本点就行了：

```python
from pywinauto.application import Application
app = Application(backend="uia").connect(title="flag 自动机")
window = app.window()
window["狠心夺取"].click()
```

然后发现居然还要什么管理员权限，反正是虚拟机，给吧。然后给了也没用，我都开始怀疑是不是我用 Windows 11 跟这个程序不兼容了……

### 反编译和 WinDbg

用 `objdump -s -j .rdata flag_machine.exe` 看到从 0x40a0a4 开始有一段文本：

```
 40a0a0 01ff0000 43006f00 6e006700 72006100  ....C.o.n.g.r.a.
 40a0b0 74007500 6c006100 74006900 6f006e00  t.u.l.a.t.i.o.n.
 40a0c0 73000000 6d609c55 604fb783 975f2000  s...m`.U`O..._ .
 40a0d0 66006c00 61006700 01ff6600 6c006100  f.l.a.g...f.l.a.
 40a0e0 67002000 065cdd4f 585b3052 535f4d52  g. ..\.OX[0RS_MR
 40a0f0 8765f64e 39590b4e 84762000 66006c00  .e.N9Y.N.v .f.l.
 40a100 61006700 5f006d00 61006300 68006900  a.g._.m.a.c.h.i.
 40a110 6e006500 2e007400 78007400 20008765  n.e...t.x.t. ..e
```

UTF-16 解码出来是 `Congratulations\x00恭喜你获得 flag！flag 将保存到当前文件夹下的 flag_machine.txt` ……

用 `objdump -d flag_machine.exe` 反汇编，看到读这个内存位置的只有一处：

```
  40185d:       c7 44 24 08 a4 a0 40    movl   $0x40a0a4,0x8(%esp)
```

往前翻翻条件跳转指令，这里非常可疑：

```
  40180a:       81 7d 14 52 bf 01 00    cmpl   $0x1bf52,0x14(%ebp)
  401811:       74 2d                   je     0x401840
```

直接 `gdb` 到这里改分支看看…… 下载了个 MSYS2，不懂为啥 `gdb` 调试这个程序的话 GUI 就出不来。于是我又从 Microsoft Store 下载了个 [WinDbg Preview](https://apps.microsoft.com/store/detail/windbg-preview/9PGJGD53TN86?hl=en-us&gl=us)，这次能调试了。的确就是那个位置的条件跳转：

```
bp 0x401811  # 加断点，继续执行程序，同时运行点击脚本
r ZF=1       # 改寄存器，使得条件成立
# 继续运行，就成功获得 flag 了
```

`flag{Y0u_rea1ly_kn0w_Win32API_...}` —— I really don't know Win32 API.





