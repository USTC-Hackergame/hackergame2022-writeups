from os import chmod
import shutil
import subprocess
import base64
import secrets

TIMEOUT = 10

if __name__ == "__main__":
    expected_stdout = secrets.token_hex(32)
    with open("/flag") as f:
        flag = f.read().strip()
    binary = input("Base64 of binary: ")
    file1, file2 = binary.split("@", 1)
    # A: secret, no I/O
    with open("/home/pwn/A/exe", "wb") as f:
        f.write(base64.b64decode(file1))
    # B: no secret, with I/O
    with open("/home/pwn/B/exe", "wb") as f:
        f.write(base64.b64decode(file2))
    chmod("/home/pwn/A/exe", 0o555)
    chmod("/home/pwn/B/exe", 0o555)
    with open("/home/pwn/A/secret", "w") as f:
        f.write(expected_stdout)
    p1 = subprocess.Popen(
        ["chroot", "--userspec=pwn:pwn", "/home/pwn/A/", "./executor", "./exe"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        p2 = subprocess.run(
            ["chroot", "--userspec=pwn:pwn", "/home/pwn/B/", "./executor", "./exe"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=TIMEOUT
        )
    except subprocess.TimeoutExpired as e:
        p1.kill()
        p2 = e
    # (variable) p2: CompletedProcess[bytes] | TimeoutExpired
    stdout = p2.stdout[:8192].decode() if p2.stdout else ""
    stderr = p2.stderr[:8192].decode() if p2.stderr else ""
    if stdout.strip() == expected_stdout:
        print(f"验证成功。{flag}")
        print("")
    else:
        print(f"验证失败。预期值为 {expected_stdout}")
        print("A 中的 /secret 每次执行都会重新生成，请再接再厉。")
        print("")
    print("stdout (原始标准输出，前 8192 个字节，以 Python bytes 格式显示):")
    print(stdout.encode())
    print("stderr (原始标准错误，前 8192 个字节，以 Python bytes 格式显示):")
    print(stderr.encode())
