import subprocess
import base64

if __name__ == "__main__":
    binary = input("Base64 of binary: ")
    with open("/dev/shm/a.exe", "wb") as f:
        f.write(base64.b64decode(binary))
    # check if it is a PE binary
    with open("/dev/shm/a.exe", "rb") as f:
        if f.read(2) != b"MZ":
            print("Not a valid PE binary.")
            exit(1)
    output = subprocess.run(
        ["su", "nobody", "-s", "/bin/bash", "-c" "/usr/bin/wine /dev/shm/a.exe"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={
            "WINEPREFIX": "/wine"
        }
    )
    stdout = output.stdout[:8192].decode()
    stderr = output.stderr.decode()
    print("stdout (标准输出，前 8192 个字节):")
    print(stdout)
    print("stderr (标准错误，前 8192 个字节):")
    stderr = stderr.split("\n")

    stderr_blacklist = [
        "it looks like wine32 is missing",
        "multiarch needs to be",
        "dpkg --add-architecture",
        "install wine32",
        "wineserver:",
        r'Failed to create directory L"C:\\users\\nobody',
    ]
    limit = 8192
    for i in stderr:
        flag = True
        for b in stderr_blacklist:
            if b in i:
                flag = False
                break
        if flag:
            i_bytes = i.encode()
            if len(i_bytes) <= limit:
                print(i)
                limit -= len(i_bytes)
            else:
                i = i_bytes[:limit].decode()
                print(i)
                exit(0)
