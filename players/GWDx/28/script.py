allCommand = []

length = 64

nums = [0] * length

page = 3
nums[1] = 9

numString = ' '.join([str(i) for i in nums])

allCommand.append(f'w T {length+1} {page} {numString}')
allCommand.append('r T 128')

allCommand.append('w 1 1 1')  # 两边写 1
allCommand.append('w 1 1 1')  # 两边写 0
allCommand.append('w 7 1 0')  # 两边写 1    7 为 0
allCommand.append('w 3 1 1')  # 两边写 2
allCommand.append('w 9 1 0')  # 两边写 0    8 9 0 为 0
allCommand.append('w 2 1 0')  # 两边写 0    1 2 3 为 0
allCommand.append('w 5 1 0')  # 两边写 0    4 5 6 为 0

for i in range(36):
    c = chr(i + 48)
    allCommand.append(f'r {c} 1')

print(numString)

with open('input.txt', 'w') as f:
    f.write('\n'.join(allCommand))

import communicate
