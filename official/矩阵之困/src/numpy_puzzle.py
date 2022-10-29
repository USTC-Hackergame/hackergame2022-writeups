import numpy as np

print('Please input 48x48 0/1 matrix:')

data = np.zeros((48, 48), dtype=bool)
for i in range(48):
    line = input()
    for j in range(48):
        if line[j] == '1':
            data[i][j] = True

d = data.astype(np.uint32)
t1 = np.einsum('ax,bx,cx->abc', d[:16], d[16:32], d[32:]) % 2
t2 = np.identity(16, dtype=bool).reshape(16, 4, 4)
t3 = np.einsum('aij,bjk->abik', t2, t2)
if (t1.reshape(-1) == t3.reshape(-1)).all():
    print(open('/flag').read())
else:
    print('Not equal')
