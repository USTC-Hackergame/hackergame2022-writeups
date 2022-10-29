import sys
import subprocess
import os

def welcome():
    banner = r'''
                _ _  _____      _ _ ____             _    
               (_) |/ ____|    | | |  _ \           | |   
      _____   ___| | |     __ _| | | |_) | __ _  ___| | __
     / _ \ \ / / | | |    / _` | | |  _ < / _` |/ __| |/ /
    |  __/\ V /| | | |___| (_| | | | |_) | (_| | (__|   < 
     \___| \_/ |_|_|\_____\__,_|_|_|____/ \__,_|\___|_|\_\
    '''
    print("\033[1;31;2m")
    print(banner)
    print("\033[0m")

def main():
    welcome()
    print("[*] Please input your code which ends with <EOF> :  ")
    code = []
    while 1:
        tmp_line = input()
        if "<EOF>" in tmp_line:
            break
        code.append(tmp_line)

    os.system("rm -rf /dev/shm/play && mkdir -m777 -p /dev/shm/play")

    with open("/dev/shm/play/attack.js", "w") as fd:
        for lines in code:
            fd.write(lines)
            fd.write("\n")

    subprocess.run(["su", "nobody", "-s", "/bin/bash", "-c" "/tmp/game/d8 --max-heap-size 1024 /dev/shm/play/attack.js"])

    sys.stdout.flush()
    sys.stderr.flush()



if __name__ == '__main__':
    main()
