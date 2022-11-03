// frida -l q12_Flag自动机.js flag_machine.exe

// 挂钩让按钮乱飘的函数，阻止按钮乱飘
// 虽然不知道为什么，但是确实能起作用（
Interceptor.attach(ptr(0x004019FA), {
    onEnter(args) {}
})

// 挂钩按下按钮的处理函数，把第四个参数改成 114514
// （这么臭的检查有什么检查的必要吗（恼（
Interceptor.attach(ptr(0x00401510), {
    onEnter(args) {
        if (args[1].toInt32() !== 0x111) {
            return
        }
        console.log("------------------------------------------------")
        for (let i=0; i<4; i++) {
            console.log(`args[${i}]: ${args[i]}, ${args[i].toInt32()}`)
        }
        args[3] = ptr("114514")
        console.log("args[3] = ", args[3].toInt32())
        console.log("------------------------------------------------")
    }
})
