import os

flag1 = "fake{test1}"
flag2 = "fake{test2}"

path1 = "/dev/shm/flag1"
path2 = "/dev/shm/flag2"

try:
    with open(path1, 'r') as f:
        flag1 = f.read()
    os.remove(path1)
except:
    raise Exception('Import flags failed, please connect developer.')

try:
    with open(path2, 'r') as f:
        flag2 = f.read()
    os.remove(path2)
except:
    raise Exception('Import flags failed, please connect developer.')
